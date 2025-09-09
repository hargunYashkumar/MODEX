import unittest
import json
from app import create_app, db
from app.models.resume_model import Resume

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_resume_creation(self):
        """Test creating a resume instance"""
        with self.app.app_context():
            resume = Resume()
            resume.full_name = "John Doe"
            resume.email = "john@example.com"
            resume.phone = "(555) 123-4567"
            resume.summary = "Software engineer"
            
            db.session.add(resume)
            db.session.commit()
            
            # Test that resume was saved
            saved_resume = Resume.query.filter_by(email="john@example.com").first()
            self.assertIsNotNone(saved_resume)
            self.assertEqual(saved_resume.full_name, "John Doe")
            self.assertEqual(saved_resume.email, "john@example.com")
    
    def test_resume_to_dict(self):
        """Test converting resume to dictionary"""
        with self.app.app_context():
            resume = Resume()
            resume.full_name = "Jane Smith"
            resume.email = "jane@example.com"
            resume.experience = json.dumps([
                {
                    'company': 'Tech Corp',
                    'position': 'Developer',
                    'duration': '2020-2023'
                }
            ])
            resume.skills = json.dumps(['Python', 'JavaScript'])
            
            resume_dict = resume.to_dict()
            
            self.assertEqual(resume_dict['full_name'], "Jane Smith")
            self.assertEqual(resume_dict['email'], "jane@example.com")
            self.assertEqual(len(resume_dict['experience']), 1)
            self.assertEqual(resume_dict['experience'][0]['company'], 'Tech Corp')
            self.assertEqual(resume_dict['skills'], ['Python', 'JavaScript'])
    
    def test_resume_from_dict(self):
        """Test creating resume from dictionary"""
        with self.app.app_context():
            data = {
                'full_name': 'Bob Johnson',
                'email': 'bob@example.com',
                'phone': '(555) 987-6543',
                'summary': 'Data scientist',
                'experience': [
                    {
                        'company': 'Data Corp',
                        'position': 'Analyst',
                        'duration': '2019-2022',
                        'description': 'Analyzed data'
                    }
                ],
                'education': [
                    {
                        'institution': 'University',
                        'degree': 'BS Computer Science',
                        'year': '2019'
                    }
                ],
                'skills': ['Python', 'SQL', 'R'],
                'projects': [],
                'certifications': ['AWS Certified'],
                'languages': ['English', 'Spanish'],
                'template_id': 'template2'
            }
            
            resume = Resume.from_dict(data)
            
            self.assertEqual(resume.full_name, 'Bob Johnson')
            self.assertEqual(resume.email, 'bob@example.com')
            self.assertEqual(resume.template_id, 'template2')
            
            # Test JSON fields
            experience = json.loads(resume.experience)
            self.assertEqual(len(experience), 1)
            self.assertEqual(experience[0]['company'], 'Data Corp')
            
            skills = json.loads(resume.skills)
            self.assertEqual(skills, ['Python', 'SQL', 'R'])
    
    def test_resume_repr(self):
        """Test resume string representation"""
        with self.app.app_context():
            resume = Resume()
            resume.full_name = "Test User"
            
            self.assertEqual(str(resume), '<Resume Test User>')
    
    def test_resume_empty_json_fields(self):
        """Test handling empty JSON fields"""
        with self.app.app_context():
            resume = Resume()
            resume.full_name = "Empty Fields"
            resume.email = "empty@example.com"
            
            resume_dict = resume.to_dict()
            
            # Should return empty lists for null JSON fields
            self.assertEqual(resume_dict['experience'], [])
            self.assertEqual(resume_dict['education'], [])
            self.assertEqual(resume_dict['skills'], [])
            self.assertEqual(resume_dict['projects'], [])
            self.assertEqual(resume_dict['certifications'], [])
            self.assertEqual(resume_dict['languages'], [])
    
    def test_resume_json_field_validation(self):
        """Test JSON field handling with valid data"""
        with self.app.app_context():
            resume = Resume()
            resume.full_name = "JSON Test"
            resume.email = "json@example.com"
            
            # Test setting JSON fields
            test_experience = [{'company': 'Test', 'position': 'Tester'}]
            test_skills = ['Testing', 'Quality Assurance']
            
            resume.experience = json.dumps(test_experience)
            resume.skills = json.dumps(test_skills)
            
            db.session.add(resume)
            db.session.commit()
            
            # Retrieve and test
            saved_resume = Resume.query.filter_by(email="json@example.com").first()
            resume_dict = saved_resume.to_dict()
            
            self.assertEqual(resume_dict['experience'], test_experience)
            self.assertEqual(resume_dict['skills'], test_skills)
    
    def test_resume_timestamps(self):
        """Test created_at and updated_at timestamps"""
        with self.app.app_context():
            resume = Resume()
            resume.full_name = "Timestamp Test"
            resume.email = "timestamp@example.com"
            
            db.session.add(resume)
            db.session.commit()
            
            # Check that timestamps were set
            self.assertIsNotNone(resume.created_at)
            self.assertIsNotNone(resume.updated_at)
            
            original_updated = resume.updated_at
            
            # Update resume
            resume.summary = "Updated summary"
            db.session.commit()
            
            # updated_at should change (though might be same second in fast tests)
            self.assertGreaterEqual(resume.updated_at, original_updated)
    
    def test_resume_query_by_template(self):
        """Test querying resumes by template"""
        with self.app.app_context():
            # Create resumes with different templates
            resume1 = Resume()
            resume1.full_name = "User 1"
            resume1.email = "user1@example.com"
            resume1.template_id = "template1"
            
            resume2 = Resume()
            resume2.full_name = "User 2"
            resume2.email = "user2@example.com"
            resume2.template_id = "template2"
            
            resume3 = Resume()
            resume3.full_name = "User 3"
            resume3.email = "user3@example.com"
            resume3.template_id = "template1"
            
            db.session.add_all([resume1, resume2, resume3])
            db.session.commit()
            
            # Query by template
            template1_resumes = Resume.query.filter_by(template_id="template1").all()
            template2_resumes = Resume.query.filter_by(template_id="template2").all()
            
            self.assertEqual(len(template1_resumes), 2)
            self.assertEqual(len(template2_resumes), 1)
    
    def test_resume_file_path(self):
        """Test file_path field for uploaded resumes"""
        with self.app.app_context():
            resume = Resume()
            resume.full_name = "File Test"
            resume.email = "file@example.com"
            resume.file_path = "/uploads/test_resume.pdf"
            
            db.session.add(resume)
            db.session.commit()
            
            saved_resume = Resume.query.filter_by(email="file@example.com").first()
            self.assertEqual(saved_resume.file_path, "/uploads/test_resume.pdf")

if __name__ == '__main__':
    unittest.main()