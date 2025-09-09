from typing import Dict, List, Any
import re
from transformers import pipeline

class DataProcessor:
    def __init__(self):
        # Initialize text processing pipeline if available
        try:
            self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        except Exception:
            self.summarizer = None
    
    def process_raw_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw form data into structured format"""
        processed_data = {}
        
        # Clean and validate basic fields
        processed_data['full_name'] = self._clean_text(data.get('full_name', ''))
        processed_data['email'] = self._validate_email(data.get('email', ''))
        processed_data['phone'] = self._format_phone(data.get('phone', ''))
        processed_data['address'] = self._clean_text(data.get('address', ''))
        processed_data['linkedin'] = self._validate_url(data.get('linkedin', ''))
        processed_data['github'] = self._validate_url(data.get('github', ''))
        processed_data['website'] = self._validate_url(data.get('website', ''))
        processed_data['summary'] = self._process_summary(data.get('summary', ''))
        
        # Process arrays
        processed_data['experience'] = self._process_experience(data.get('experience', []))
        processed_data['education'] = self._process_education(data.get('education', []))
        processed_data['skills'] = self._process_skills(data.get('skills', []))
        processed_data['projects'] = self._process_projects(data.get('projects', []))
        processed_data['certifications'] = self._process_certifications(data.get('certifications', []))
        processed_data['languages'] = self._process_languages(data.get('languages', []))
        
        processed_data['template_id'] = data.get('template_id', 'template1')
        
        return processed_data
    
    def process_parsed_data(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data that was parsed from a resume file"""
        # Similar processing but with different validation since data comes from parsing
        processed_data = {}
        
        processed_data['full_name'] = self._clean_text(parsed_data.get('full_name', ''))
        processed_data['email'] = parsed_data.get('email', '')
        processed_data['phone'] = parsed_data.get('phone', '')
        processed_data['address'] = self._clean_text(parsed_data.get('address', ''))
        processed_data['linkedin'] = parsed_data.get('linkedin', '')
        processed_data['github'] = parsed_data.get('github', '')
        processed_data['website'] = parsed_data.get('website', '')
        processed_data['summary'] = self._improve_summary(parsed_data.get('summary', ''))
        
        # Process parsed arrays
        processed_data['experience'] = self._enhance_experience(parsed_data.get('experience', []))
        processed_data['education'] = self._enhance_education(parsed_data.get('education', []))
        processed_data['skills'] = self._categorize_skills(parsed_data.get('skills', []))
        processed_data['projects'] = self._enhance_projects(parsed_data.get('projects', []))
        processed_data['certifications'] = parsed_data.get('certifications', [])
        processed_data['languages'] = parsed_data.get('languages', [])
        
        processed_data['template_id'] = parsed_data.get('template_id', 'template1')
        
        return processed_data
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = ' '.join(text.split())
        return text.strip()
    
    def _validate_email(self, email: str) -> str:
        """Validate email format"""
        if not email:
            return ""
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, email):
            return email.lower()
        return ""
    
    def _format_phone(self, phone: str) -> str:
        """Format phone number"""
        if not phone:
            return ""
        
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        
        return phone  # Return original if can't format
    
    def _validate_url(self, url: str) -> str:
        """Validate and format URL"""
        if not url:
            return ""
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return url
    
    def _process_summary(self, summary: str) -> str:
        """Process professional summary"""
        if not summary:
            return ""
        
        summary = self._clean_text(summary)
        
        # Ensure summary is not too long (limit to 500 characters)
        if len(summary) > 500:
            summary = summary[:500].rstrip() + "..."
        
        return summary
    
    def _improve_summary(self, summary: str) -> str:
        """Improve parsed summary using AI if available"""
        if not summary:
            return ""
        
        summary = self._clean_text(summary)
        
        # If summarizer is available and text is long enough, improve it
        if self.summarizer and len(summary) > 200:
            try:
                improved = self.summarizer(summary, max_length=150, min_length=50, do_sample=False)
                return improved[0]['summary_text']
            except Exception:
                pass
        
        return summary
    
    def _process_experience(self, experience: List[Dict]) -> List[Dict]:
        """Process work experience data"""
        processed = []
        
        for exp in experience:
            if not exp.get('company'):
                continue
            
            processed_exp = {
                'company': self._clean_text(exp.get('company', '')),
                'position': self._clean_text(exp.get('position', '')),
                'duration': self._clean_text(exp.get('duration', '')),
                'description': self._clean_text(exp.get('description', ''))
            }
            
            if processed_exp['company']:  # Only add if company name exists
                processed.append(processed_exp)
        
        return processed
    
    def _enhance_experience(self, experience: List[Dict]) -> List[Dict]:
        """Enhance parsed experience data"""
        enhanced = []
        
        for exp in experience:
            enhanced_exp = {
                'company': self._clean_text(exp.get('company', '')),
                'position': self._clean_text(exp.get('position', '')),
                'duration': self._standardize_duration(exp.get('duration', '')),
                'description': self._enhance_description(exp.get('description', ''))
            }
            
            if enhanced_exp['company']:
                enhanced.append(enhanced_exp)
        
        return enhanced
    
    def _process_education(self, education: List[Dict]) -> List[Dict]:
        """Process education data"""
        processed = []
        
        for edu in education:
            if not edu.get('institution'):
                continue
            
            processed_edu = {
                'institution': self._clean_text(edu.get('institution', '')),
                'degree': self._clean_text(edu.get('degree', '')),
                'year': self._clean_text(edu.get('year', '')),
                'gpa': self._clean_text(edu.get('gpa', ''))
            }
            
            if processed_edu['institution']:
                processed.append(processed_edu)
        
        return processed
    
    def _enhance_education(self, education: List[Dict]) -> List[Dict]:
        """Enhance parsed education data"""
        enhanced = []
        
        for edu in education:
            enhanced_edu = {
                'institution': self._clean_text(edu.get('institution', '')),
                'degree': self._standardize_degree(edu.get('degree', '')),
                'year': self._extract_year(edu.get('year', '')),
                'gpa': self._format_gpa(edu.get('gpa', ''))
            }
            
            if enhanced_edu['institution']:
                enhanced.append(enhanced_edu)
        
        return enhanced
    
    def _process_skills(self, skills: List[str]) -> List[str]:
        """Process skills list"""
        processed = []
        
        for skill in skills:
            skill = self._clean_text(skill)
            if skill and skill.lower() not in [s.lower() for s in processed]:
                processed.append(skill)
        
        return processed
    
    def _categorize_skills(self, skills: List[str]) -> List[str]:
        """Categorize and clean skills"""
        skill_categories = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'kotlin'],
            'web': ['html', 'css', 'react', 'vue', 'angular', 'node.js', 'django', 'flask', 'express'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
            'tools': ['git', 'jenkins', 'jira', 'confluence']
        }
        
        processed = []
        for skill in skills:
            skill = self._clean_text(skill)
            if skill and skill.lower() not in [s.lower() for s in processed]:
                processed.append(skill)
        
        return processed
    
    def _process_projects(self, projects: List[Dict]) -> List[Dict]:
        """Process projects data"""
        processed = []
        
        for proj in projects:
            if not proj.get('name'):
                continue
            
            processed_proj = {
                'name': self._clean_text(proj.get('name', '')),
                'description': self._clean_text(proj.get('description', '')),
                'technologies': self._clean_text(proj.get('technologies', '')),
                'url': self._validate_url(proj.get('url', ''))
            }
            
            if processed_proj['name']:
                processed.append(processed_proj)
        
        return processed
    
    def _enhance_projects(self, projects: List[Dict]) -> List[Dict]:
        """Enhance parsed projects data"""
        enhanced = []
        
        for proj in projects:
            enhanced_proj = {
                'name': self._clean_text(proj.get('name', '')),
                'description': self._enhance_description(proj.get('description', '')),
                'technologies': self._extract_technologies(proj.get('description', '')),
                'url': proj.get('url', '')
            }
            
            if enhanced_proj['name']:
                enhanced.append(enhanced_proj)
        
        return enhanced
    
    def _process_certifications(self, certifications: List[str]) -> List[str]:
        """Process certifications list"""
        processed = []
        
        for cert in certifications:
            cert = self._clean_text(cert)
            if cert and cert not in processed:
                processed.append(cert)
        
        return processed
    
    def _process_languages(self, languages: List[str]) -> List[str]:
        """Process languages list"""
        processed = []
        
        for lang in languages:
            lang = self._clean_text(lang)
            if lang and lang not in processed:
                processed.append(lang)
        
        return processed
    
    def _standardize_duration(self, duration: str) -> str:
        """Standardize date duration format"""
        if not duration:
            return ""
        
        # Try to extract years and format consistently
        years = re.findall(r'\d{4}', duration)
        if len(years) >= 2:
            return f"{years[0]} - {years[-1]}"
        elif len(years) == 1:
            if 'present' in duration.lower() or 'current' in duration.lower():
                return f"{years[0]} - Present"
        
        return duration
    
    def _standardize_degree(self, degree: str) -> str:
        """Standardize degree format"""
        if not degree:
            return ""
        
        # Common degree abbreviations
        degree_map = {
            'bs': 'Bachelor of Science',
            'ba': 'Bachelor of Arts',
            'ms': 'Master of Science', 
            'ma': 'Master of Arts',
            'mba': 'Master of Business Administration',
            'phd': 'Doctor of Philosophy'
        }
        
        degree_lower = degree.lower()
        for abbr, full in degree_map.items():
            if abbr in degree_lower:
                return full
        
        return degree
    
    def _extract_year(self, year_text: str) -> str:
        """Extract year from text"""
        if not year_text:
            return ""
        
        years = re.findall(r'\d{4}', year_text)
        return years[0] if years else year_text
    
    def _format_gpa(self, gpa_text: str) -> str:
        """Format GPA consistently"""
        if not gpa_text:
            return ""
        
        # Extract GPA number
        gpa_match = re.search(r'(\d+\.?\d*)', gpa_text)
        if gpa_match:
            gpa = float(gpa_match.group(1))
            if gpa <= 4.0:
                return f"{gpa:.1f}/4.0"
            elif gpa <= 100:
                return f"{gpa:.0f}/100"
        
        return gpa_text
    
    def _enhance_description(self, description: str) -> str:
        """Enhance job/project descriptions"""
        if not description:
            return ""
        
        description = self._clean_text(description)
        
        # Ensure description starts with action verb
        action_verbs = ['developed', 'implemented', 'designed', 'created', 'managed', 'led', 'built', 'optimized']
        first_word = description.split()[0].lower() if description.split() else ""
        
        if first_word not in action_verbs and len(description) > 20:
            # Add a generic action verb if missing
            description = "Developed " + description.lower()
        
        return description
    
    def _extract_technologies(self, text: str) -> str:
        """Extract technologies from project description"""
        if not text:
            return ""
        
        common_techs = [
            'python', 'java', 'javascript', 'react', 'node.js', 'angular', 'vue',
            'html', 'css', 'sql', 'mongodb', 'postgresql', 'mysql', 'docker',
            'kubernetes', 'aws', 'azure', 'git', 'django', 'flask', 'express'
        ]
        
        found_techs = []
        text_lower = text.lower()
        
        for tech in common_techs:
            if tech in text_lower:
                found_techs.append(tech.title())
        
        return ', '.join(found_techs) if found_techs else ""