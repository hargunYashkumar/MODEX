from typing import Dict, Any
from jinja2 import Template
import os
from flask import current_app, render_template

class TemplateGenerator:
    def __init__(self):
        self.templates = {
            'template1': 'resume_templates/template1.html',
            'template2': 'resume_templates/template2.html',
            'template3': 'resume_templates/template3.html'
        }
    
    def generate_resume(self, resume_data: Dict[str, Any]) -> str:
        """Generate resume HTML from data using specified template"""
        try:
            template_id = resume_data.get('template_id', 'template1')
            template_path = self.templates.get(template_id, self.templates['template1'])
            
            # Render the template with resume data
            return render_template(template_path, resume=resume_data)
            
        except Exception as e:
            raise Exception(f"Error generating resume: {str(e)}")
    
    def get_available_templates(self) -> Dict[str, str]:
        """Return available templates"""
        return {
            'template1': 'Professional Template',
            'template2': 'Modern Template', 
            'template3': 'Creative Template'
        }
    
    def preview_template(self, template_id: str) -> str:
        """Generate a preview of the template with sample data"""
        sample_data = {
            'full_name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '(555) 123-4567',
            'address': '123 Main St, City, State 12345',
            'linkedin': 'https://linkedin.com/in/johndoe',
            'github': 'https://github.com/johndoe',
            'website': 'https://johndoe.dev',
            'summary': 'Experienced software developer with expertise in web technologies and problem-solving.',
            'experience': [
                {
                    'company': 'Tech Corp',
                    'position': 'Senior Developer',
                    'duration': '2020 - Present',
                    'description': 'Led development of web applications using modern technologies.'
                },
                {
                    'company': 'StartUp Inc',
                    'position': 'Junior Developer',
                    'duration': '2018 - 2020',
                    'description': 'Developed and maintained web applications.'
                }
            ],
            'education': [
                {
                    'institution': 'University of Technology',
                    'degree': 'Bachelor of Science in Computer Science',
                    'year': '2018',
                    'gpa': '3.8/4.0'
                }
            ],
            'skills': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL', 'Git'],
            'projects': [
                {
                    'name': 'E-commerce Platform',
                    'description': 'Built a full-stack e-commerce platform with React and Node.js',
                    'technologies': 'React, Node.js, MongoDB',
                    'url': 'https://github.com/johndoe/ecommerce'
                }
            ],
            'certifications': ['AWS Certified Developer', 'Google Cloud Professional'],
            'languages': ['English (Native)', 'Spanish (Conversational)'],
            'template_id': template_id
        }
        
        return self.generate_resume(sample_data)