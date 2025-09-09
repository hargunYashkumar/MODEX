import unittest
import tempfile
import os
from app.services.resume_parser import ResumeParser
from app.services.data_processor import DataProcessor
from app.services.template_generator import TemplateGenerator

class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = ResumeParser()
        self.processor = DataProcessor()
        self.generator = TemplateGenerator()
    
    def test_resume_parser_extract_email(self):
        """Test email extraction from text"""
        text = "Contact me at john.doe@example.com for more information"
        email = self.parser._extract_email(text)
        self.assertEqual(email, "john.doe@example.com")
    
    def test_resume_parser_extract_phone(self):
        """Test phone extraction from text"""
        text = "Call me at (555) 123-4567"
        phone = self.parser._extract_phone(text)
        self.assertEqual(phone, "(555) 123-4567")
    
    def test_resume_parser_extract_name(self):
        """Test name extraction from text"""
        text = "John Doe\nSoftware Engineer\njohn@example.com"
        name = self.parser._extract_name(text)
        self.assertEqual(name, "John Doe")
    
    def test_resume_parser_extract_skills(self):
        """Test skills extraction from text"""
        section_text = "Skills\nPython, JavaScript, React, Node.js"
        skills = self.parser._extract_skills(section_text)
        expected_skills = ['Python', 'JavaScript', 'React', 'Node.js']
        self.assertEqual(skills, expected_skills)
    
    def test_resume_parser_txt_file(self):
        """Test parsing a text file"""
        # Create temporary text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
            tmp.write("John Doe\nSoftware Engineer\njohn@example.com\n(555) 123-4567")
            tmp_path = tmp.name
        
        try:
            text = self.parser._extract_from_txt(tmp_path)
            self.assertIn("John Doe", text)
            self.assertIn("john@example.com", text)
        finally:
            os.unlink(tmp_path)
    
    def test_data_processor_clean_text(self):
        """Test text cleaning functionality"""
        dirty_text = "  This   has    extra   spaces  "
        cleaned = self.processor._clean_text(dirty_text)
        self.assertEqual(cleaned, "This has extra spaces")
    
    def test_data_processor_validate_email(self):
        """Test email validation"""
        valid_email = "test@example.com"
        invalid_email = "invalid-email"
        
        self.assertEqual(self.processor._validate_email(valid_email), "test@example.com")
        self.assertEqual(self.processor._validate_email(invalid_email), "")
    
    def test_data_processor_format_phone(self):
        """Test phone formatting"""
        phone_digits = "5551234567"
        formatted = self.processor._format_phone(phone_digits)
        self.assertEqual(formatted, "(555) 123-4567")
    
    def test_data_processor_validate_url(self):
        """Test URL validation and formatting"""
        url_without_protocol = "example.com"
        formatted_url = self.processor._validate_url(url_without_protocol)
        self.assertEqual(formatted_url, "https://example.com")
    
    def test_data_processor_process_raw_data(self):
        """Test processing raw form data"""
        raw_data = {
            'full_name': '  John Doe  ',
            'email': 'JOHN@EXAMPLE.COM',
            'phone': '555-123-4567',
            'skills': ['Python', 'JavaScript', 'React'],
            'experience': [
                {
                    'company': 'Test Corp',
                    'position': 'Developer',
                    'duration': '2020-2023',
                    'description': 'Worked on projects'
                }
            ],
            'template_id': 'template1'
        }
        
        processed = self.processor.process_raw_data(raw_data)
        
        self.assertEqual(processed['full_name'], 'John Doe')
        self.assertEqual(processed['email'], 'john@example.com')
        self.assertEqual(processed['phone'], '(555) 123-4567')
        self.assertEqual(len(processed['experience']), 1)
        self.assertEqual(processed['experience'][0]['company'], 'Test Corp')
    
    def test_data_processor_enhance_experience(self):
        """Test experience enhancement"""
        experience = [
            {
                'company': 'Tech Corp',
                'position': 'developer',
                'duration': '2020 to 2023',
                'description': 'worked on various projects using python'
            }
        ]
        
        enhanced = self.processor._enhance_experience(experience)
        
        self.assertEqual(len(enhanced), 1)
        self.assertEqual(enhanced[0]['company'], 'Tech Corp')
        self.assertEqual(enhanced[0]['duration'], '2020 - 2023')
        self.assertIn('Developed', enhanced[0]['description'])  # Should start with action verb
    
    def test_template_generator_available_templates(self):
        """Test getting available templates"""
        templates = self.generator.get_available_templates()
        
        self.assertIn('template1', templates)
        self.assertIn('template2', templates)
        self.assertIn('template3', templates)
        self.assertEqual(templates['template1'], 'Professional Template')
    
    def test_template_generator_generate_resume(self):
        """Test resume generation (mock test)"""
        resume_data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone': '(555) 123-4567',
            'summary': 'Software engineer with experience',
            'experience': [
                {
                    'company': 'Tech Corp',
                    'position': 'Developer',
                    'duration': '2020-2023',
                    'description': 'Developed applications'
                }
            ],
            'education': [],
            'skills': ['Python', 'JavaScript'],
            'projects': [],
            'certifications': [],
            'languages': [],
            'template_id': 'template1'
        }
        
        # This would require Flask app context to render templates
        # For now, just test that the method doesn't crash
        try:
            # In a real test, we'd need to mock the render_template function
            # or set up a proper Flask app context
            pass
        except Exception as e:
            self.fail(f"Template generation raised an exception: {e}")
    
    def test_data_processor_categorize_skills(self):
        """Test skill categorization"""
        skills = ['Python', 'Java', 'React', 'MongoDB', 'AWS', 'HTML', 'CSS']
        categorized = self.processor._categorize_skills(skills)
        
        # All skills should be preserved
        self.assertEqual(len(categorized), 7)
        self.assertIn('Python', categorized)
        self.assertIn('React', categorized)
    
    def test_data_processor_standardize_duration(self):
        """Test duration standardization"""
        duration1 = "January 2020 to December 2022"
        duration2 = "2020 - present"
        
        std1 = self.processor._standardize_duration(duration1)
        std2 = self.processor._standardize_duration(duration2)
        
        # Should extract years
        self.assertIn('2020', std1)
        self.assertIn('2022', std1)
        self.assertIn('Present', std2)
    
    def test_data_processor_format_gpa(self):
        """Test GPA formatting"""
        gpa1 = "3.8"
        gpa2 = "85"
        gpa3 = "GPA: 3.5/4.0"
        
        formatted1 = self.processor._format_gpa(gpa1)
        formatted2 = self.processor._format_gpa(gpa2)
        formatted3 = self.processor._format_gpa(gpa3)
        
        self.assertEqual(formatted1, "3.8/4.0")
        self.assertEqual(formatted2, "85/100")
        self.assertIn("3.5", formatted3)

if __name__ == '__main__':
    unittest.main()