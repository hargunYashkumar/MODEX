import unittest
import json
import os
from app import create_app, db
from app.models.resume_model import Resume

class RouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_home_page(self):
        """Test home page loads correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Resume Generator', response.data)
    
    def test_raw_data_form_page(self):
        """Test raw data form page loads correctly"""
        response = self.client.get('/raw-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Your Resume', response.data)
    
    def test_upload_form_page(self):
        """Test upload form page loads correctly"""
        response = self.client.get('/upload')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload Your Resume', response.data)
    
    def test_process_raw_data_missing_required(self):
        """Test processing raw data with missing required fields"""
        response = self.client.post('/process-raw-data', data={
            'template_id': 'template1'
            # Missing required fields like full_name, email
        })
        # Should redirect back to form or show error
        self.assertIn(response.status_code, [302, 400])
    
    def test_process_raw_data_success(self):
        """Test successful raw data processing"""
        data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'summary': 'Test summary',
            'template_id': 'template1',
            'skills': 'Python, JavaScript',
            'experience_company_0': 'Test Corp',
            'experience_position_0': 'Developer',
            'experience_duration_0': '2020-2023',
            'experience_description_0': 'Worked on various projects'
        }
        
        response = self.client.post('/process-raw-data', data=data)
        
        # Should create resume and show result
        self.assertIn(response.status_code, [200, 302])
        
        # Check if resume was created in database
        with self.app.app_context():
            resume = Resume.query.filter_by(email='john@example.com').first()
            self.assertIsNotNone(resume)
            self.assertEqual(resume.full_name, 'John Doe')
    
    def test_resume_list_empty(self):
        """Test resume list page when no resumes exist"""
        response = self.client.get('/resumes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No resumes found', response.data)
    
    def test_resume_list_with_data(self):
        """Test resume list page with existing resumes"""
        # Create test resume
        with self.app.app_context():
            resume_data = {
                'full_name': 'Test User',
                'email': 'test@example.com',
                'summary': 'Test summary',
                'experience': [],
                'education': [],
                'skills': ['Python'],
                'projects': [],
                'certifications': [],
                'languages': []
            }
            
            resume = Resume.from_dict(resume_data)
            db.session.add(resume)
            db.session.commit()
            resume_id = resume.id
        
        response = self.client.get('/resumes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)
    
    def test_view_nonexistent_resume(self):
        """Test viewing a resume that doesn't exist"""
        response = self.client.get('/resume/999')
        self.assertEqual(response.status_code, 404)
    
    def test_view_existing_resume(self):
        """Test viewing an existing resume"""
        # Create test resume
        with self.app.app_context():
            resume_data = {
                'full_name': 'Test User',
                'email': 'test@example.com',
                'summary': 'Test summary',
                'experience': [],
                'education': [],
                'skills': ['Python'],
                'projects': [],
                'certifications': [],
                'languages': []
            }
            
            resume = Resume.from_dict(resume_data)
            db.session.add(resume)
            db.session.commit()
            resume_id = resume.id
        
        response = self.client.get(f'/resume/{resume_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

if __name__ == '__main__':
    unittest.main()