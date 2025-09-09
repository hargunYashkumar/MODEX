from app import db
from datetime import datetime
import json

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Personal Information
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))
    website = db.Column(db.String(200))
    
    # Professional Information
    summary = db.Column(db.Text)
    experience = db.Column(db.Text)  # JSON string
    education = db.Column(db.Text)   # JSON string
    skills = db.Column(db.Text)      # JSON string
    projects = db.Column(db.Text)    # JSON string
    certifications = db.Column(db.Text)  # JSON string
    languages = db.Column(db.Text)   # JSON string
    
    # Metadata
    template_id = db.Column(db.String(50), default='template1')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    file_path = db.Column(db.String(200))  # Original file path if uploaded
    
    def __repr__(self):
        return f'<Resume {self.full_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'linkedin': self.linkedin,
            'github': self.github,
            'website': self.website,
            'summary': self.summary,
            'experience': json.loads(self.experience) if self.experience else [],
            'education': json.loads(self.education) if self.education else [],
            'skills': json.loads(self.skills) if self.skills else [],
            'projects': json.loads(self.projects) if self.projects else [],
            'certifications': json.loads(self.certifications) if self.certifications else [],
            'languages': json.loads(self.languages) if self.languages else [],
            'template_id': self.template_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data):
        resume = Resume()
        resume.full_name = data.get('full_name', '')
        resume.email = data.get('email', '')
        resume.phone = data.get('phone', '')
        resume.address = data.get('address', '')
        resume.linkedin = data.get('linkedin', '')
        resume.github = data.get('github', '')
        resume.website = data.get('website', '')
        resume.summary = data.get('summary', '')
        
        # Convert lists to JSON strings
        resume.experience = json.dumps(data.get('experience', []))
        resume.education = json.dumps(data.get('education', []))
        resume.skills = json.dumps(data.get('skills', []))
        resume.projects = json.dumps(data.get('projects', []))
        resume.certifications = json.dumps(data.get('certifications', []))
        resume.languages = json.dumps(data.get('languages', []))
        
        resume.template_id = data.get('template_id', 'template1')
        
        return resume