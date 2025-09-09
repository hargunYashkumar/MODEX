import os
import re
from typing import Dict, List, Any
import PyPDF2
import docx
from transformers import pipeline

class ResumeParser:
    def __init__(self):
        # Initialize NLP pipeline for named entity recognition
        try:
            self.nlp = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
        except Exception:
            self.nlp = None
        
        # Common patterns for resume parsing
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            'linkedin': r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+/?',
            'github': r'(?:https?://)?(?:www\.)?github\.com/[\w-]+/?',
            'website': r'(?:https?://)?(?:www\.)?[\w.-]+\.[\w]{2,}/?'
        }
        
        # Section keywords for identifying different parts of resume
        self.section_keywords = {
            'experience': ['experience', 'work history', 'employment', 'professional experience', 'work experience'],
            'education': ['education', 'academic background', 'qualifications', 'academic qualifications'],
            'skills': ['skills', 'technical skills', 'core competencies', 'expertise', 'technologies'],
            'projects': ['projects', 'personal projects', 'key projects', 'notable projects'],
            'certifications': ['certifications', 'certificates', 'professional certifications'],
            'summary': ['summary', 'profile', 'objective', 'professional summary', 'career objective']
        }
    
    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """Main method to parse resume from file"""
        try:
            # Extract text based on file type
            text = self._extract_text(file_path)
            
            if not text:
                raise ValueError("Could not extract text from file")
            
            # Parse different sections
            parsed_data = {
                'full_name': self._extract_name(text),
                'email': self._extract_email(text),
                'phone': self._extract_phone(text),
                'linkedin': self._extract_linkedin(text),
                'github': self._extract_github(text),
                'website': self._extract_website(text),
                'summary': self._extract_summary(text),
                'experience': self._extract_experience(text),
                'education': self._extract_education(text),
                'skills': self._extract_skills(text),
                'projects': self._extract_projects(text),
                'certifications': self._extract_certifications(text),
                'languages': [],
                'address': self._extract_address(text)
            }
            
            return parsed_data
            
        except Exception as e:
            raise Exception(f"Error parsing resume: {str(e)}")
    
    def _extract_text(self, file_path: str) -> str:
        """Extract text from different file formats"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            return self._extract_from_docx(file_path)
        elif file_ext == '.txt':
            return self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
        return text
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT: {str(e)}")
        return text
    
    def _extract_name(self, text: str) -> str:
        """Extract full name from text"""
        lines = text.split('\n')
        # Usually name is in the first few lines
        for line in lines[:5]:
            line = line.strip()
            if line and not re.search(self.patterns['email'], line) and not re.search(self.patterns['phone'], line):
                # Simple heuristic: if line has 2-4 words and no numbers, likely a name
                words = line.split()
                if 2 <= len(words) <= 4 and not any(char.isdigit() for char in line):
                    return line
        return ""
    
    def _extract_email(self, text: str) -> str:
        """Extract email from text"""
        matches = re.findall(self.patterns['email'], text)
        return matches[0] if matches else ""
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number from text"""
        matches = re.findall(self.patterns['phone'], text)
        if matches:
            # Format phone number
            return f"({matches[0][0]}) {matches[0][1]}-{matches[0][2]}"
        return ""
    
    def _extract_linkedin(self, text: str) -> str:
        """Extract LinkedIn URL from text"""
        matches = re.findall(self.patterns['linkedin'], text)
        return matches[0] if matches else ""
    
    def _extract_github(self, text: str) -> str:
        """Extract GitHub URL from text"""
        matches = re.findall(self.patterns['github'], text)
        return matches[0] if matches else ""
    
    def _extract_website(self, text: str) -> str:
        """Extract website URL from text"""
        matches = re.findall(self.patterns['website'], text)
        # Filter out email domains and social media
        for match in matches:
            if not any(domain in match.lower() for domain in ['gmail', 'yahoo', 'hotmail', 'linkedin', 'github', 'facebook', 'twitter']):
                return match
        return ""
    
    def _extract_address(self, text: str) -> str:
        """Extract address from text (basic implementation)"""
        # Look for patterns that might be addresses
        lines = text.split('\n')
        for line in lines:
            # Simple check for address-like patterns
            if re.search(r'\d+.*\w+.*(?:st|street|ave|avenue|rd|road|ln|lane|dr|drive|ct|court|way|blvd|boulevard)', line, re.IGNORECASE):
                return line.strip()
        return ""
    
    def _extract_section(self, text: str, section_type: str) -> str:
        """Extract a specific section from text"""
        keywords = self.section_keywords.get(section_type, [])
        lines = text.split('\n')
        
        section_start = -1
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            if any(keyword in line_lower for keyword in keywords):
                section_start = i
                break
        
        if section_start == -1:
            return ""
        
        # Find section end (next major section or end of text)
        section_end = len(lines)
        for i in range(section_start + 1, len(lines)):
            line_lower = lines[i].lower().strip()
            # Check if this line starts another major section
            for other_section, other_keywords in self.section_keywords.items():
                if other_section != section_type and any(keyword in line_lower for keyword in other_keywords):
                    section_end = i
                    break
            if section_end != len(lines):
                break
        
        return '\n'.join(lines[section_start:section_end])
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary"""
        section_text = self._extract_section(text, 'summary')
        if section_text:
            lines = section_text.split('\n')[1:]  # Skip the header line
            return '\n'.join([line.strip() for line in lines if line.strip()])
        return ""
    
    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience"""
        section_text = self._extract_section(text, 'experience')
        experiences = []
        
        if section_text:
            # Simple parsing - look for patterns like "Company Name" followed by position and dates
            lines = section_text.split('\n')[1:]  # Skip header
            current_exp = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    if current_exp:
                        experiences.append(current_exp)
                        current_exp = {}
                    continue
                
                # Try to identify if this is a company, position, or description
                if not current_exp.get('company') and len(line.split()) <= 5:
                    current_exp['company'] = line
                elif not current_exp.get('position') and any(title in line.lower() for title in ['engineer', 'developer', 'manager', 'analyst', 'intern', 'specialist']):
                    current_exp['position'] = line
                elif re.search(r'\d{4}', line):  # Line with year, likely duration
                    current_exp['duration'] = line
                else:
                    if 'description' not in current_exp:
                        current_exp['description'] = line
                    else:
                        current_exp['description'] += ' ' + line
            
            if current_exp:
                experiences.append(current_exp)
        
        return experiences
    
    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information"""
        section_text = self._extract_section(text, 'education')
        education = []
        
        if section_text:
            lines = section_text.split('\n')[1:]
            current_edu = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    if current_edu:
                        education.append(current_edu)
                        current_edu = {}
                    continue
                
                # Identify institution, degree, year
                if any(term in line.lower() for term in ['university', 'college', 'institute', 'school']):
                    current_edu['institution'] = line
                elif any(degree in line.lower() for degree in ['bachelor', 'master', 'phd', 'bs', 'ms', 'ba', 'ma']):
                    current_edu['degree'] = line
                elif re.search(r'\d{4}', line):
                    current_edu['year'] = line
                elif 'gpa' in line.lower():
                    current_edu['gpa'] = line
            
            if current_edu:
                education.append(current_edu)
        
        return education
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills list"""
        section_text = self._extract_section(text, 'skills')
        skills = []
        
        if section_text:
            lines = section_text.split('\n')[1:]
            for line in lines:
                line = line.strip()
                if line:
                    # Split by common delimiters
                    line_skills = re.split(r'[,;•\-\|]', line)
                    skills.extend([skill.strip() for skill in line_skills if skill.strip()])
        
        return skills
    
    def _extract_projects(self, text: str) -> List[Dict[str, str]]:
        """Extract projects information"""
        section_text = self._extract_section(text, 'projects')
        projects = []
        
        if section_text:
            lines = section_text.split('\n')[1:]
            current_project = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    if current_project:
                        projects.append(current_project)
                        current_project = {}
                    continue
                
                # Simple heuristic for project parsing
                if not current_project.get('name') and len(line.split()) <= 8:
                    current_project['name'] = line
                elif 'http' in line.lower():
                    current_project['url'] = line
                else:
                    if 'description' not in current_project:
                        current_project['description'] = line
                    else:
                        current_project['description'] += ' ' + line
            
            if current_project:
                projects.append(current_project)
        
        return projects
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        section_text = self._extract_section(text, 'certifications')
        certifications = []
        
        if section_text:
            lines = section_text.split('\n')[1:]
            for line in lines:
                line = line.strip()
                if line and line not in ['certifications', 'certificates']:
                    certifications.append(line)
        
        return certifications