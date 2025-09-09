import os
import re
from typing import Dict, Any
from flask import current_app

def validate_file(file_path: str) -> Dict[str, Any]:
    """Validate uploaded file"""
    result = {'valid': True, 'error': None}
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            result['valid'] = False
            result['error'] = 'File does not exist'
            return result
        
        # Check file size
        file_size = os.path.getsize(file_path)
        max_size = current_app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)
        
        if file_size > max_size:
            result['valid'] = False
            result['error'] = f'File size exceeds maximum limit of {max_size // (1024*1024)}MB'
            return result
        
        if file_size == 0:
            result['valid'] = False
            result['error'] = 'File is empty'
            return result
        
        # Check file extension
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'docx', 'doc', 'txt'})
        file_ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        
        if file_ext not in allowed_extensions:
            result['valid'] = False
            result['error'] = f'File type .{file_ext} not allowed. Allowed types: {", ".join(allowed_extensions)}'
            return result
        
        # Basic content validation for text files
        if file_ext == 'txt':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(1000)  # Read first 1000 chars
                    if not content.strip():
                        result['valid'] = False
                        result['error'] = 'Text file appears to be empty or contains only whitespace'
                        return result
            except UnicodeDecodeError:
                result['valid'] = False
                result['error'] = 'Text file contains invalid characters'
                return result
        
        return result
        
    except Exception as e:
        result['valid'] = False
        result['error'] = f'Error validating file: {str(e)}'
        return result

def validate_resume_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate resume data structure"""
    result = {'valid': True, 'errors': []}
    
    # Required fields
    required_fields = ['full_name', 'email']
    
    for field in required_fields:
        if not data.get(field):
            result['errors'].append(f'{field.replace("_", " ").title()} is required')
    
    # Email validation
    if data.get('email'):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email']):
            result['errors'].append('Invalid email format')
    
    # Phone validation (if provided)
    if data.get('phone'):
        phone_clean = re.sub(r'\D', '', data['phone'])
        if len(phone_clean) not in [10, 11]:
            result['errors'].append('Phone number should be 10 or 11 digits')
    
    # URL validations
    url_fields = ['linkedin', 'github', 'website']
    for field in url_fields:
        if data.get(field):
            url = data[field]
            if not url.startswith(('http://', 'https://')):
                # Auto-fix by adding https://
                data[field] = 'https://' + url
    
    # Validate experience array
    if data.get('experience') and isinstance(data['experience'], list):
        for i, exp in enumerate(data['experience']):
            if not isinstance(exp, dict):
                result['errors'].append(f'Experience entry {i+1} is not properly formatted')
            elif not exp.get('company'):
                result['errors'].append(f'Experience entry {i+1} is missing company name')
    
    # Validate education array
    if data.get('education') and isinstance(data['education'], list):
        for i, edu in enumerate(data['education']):
            if not isinstance(edu, dict):
                result['errors'].append(f'Education entry {i+1} is not properly formatted')
            elif not edu.get('institution'):
                result['errors'].append(f'Education entry {i+1} is missing institution name')
    
    # Validate skills array
    if data.get('skills') and not isinstance(data['skills'], list):
        result['errors'].append('Skills should be a list')
    
    # Validate projects array
    if data.get('projects') and isinstance(data['projects'], list):
        for i, proj in enumerate(data['projects']):
            if not isinstance(proj, dict):
                result['errors'].append(f'Project entry {i+1} is not properly formatted')
            elif not proj.get('name'):
                result['errors'].append(f'Project entry {i+1} is missing project name')
    
    result['valid'] = len(result['errors']) == 0
    return result

def validate_template_id(template_id: str) -> bool:
    """Validate template ID"""
    valid_templates = ['template1', 'template2', 'template3']
    return template_id in valid_templates

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent security issues"""
    # Remove any path components
    filename = os.path.basename(filename)
    
    # Replace dangerous characters
    filename = re.sub(r'[^\w\-_\.]', '_', filename)
    
    # Limit length
    name, ext = os.path.splitext(filename)
    if len(name) > 100:
        name = name[:100]
    
    return name + ext

def validate_form_data(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate form data from web forms"""
    result = {'valid': True, 'errors': []}
    
    # Basic validation
    if not form_data.get('full_name', '').strip():
        result['errors'].append('Full name is required')
    
    if not form_data.get('email', '').strip():
        result['errors'].append('Email is required')
    else:
        email = form_data['email'].strip()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            result['errors'].append('Please enter a valid email address')
    
    # Phone validation (optional but must be valid if provided)
    phone = form_data.get('phone', '').strip()
    if phone:
        phone_digits = re.sub(r'\D', '', phone)
        if len(phone_digits) not in [10, 11]:
            result['errors'].append('Please enter a valid phone number (10-11 digits)')
    
    # URL validation
    for field in ['linkedin', 'github', 'website']:
        url = form_data.get(field, '').strip()
        if url and not url.startswith(('http://', 'https://')):
            form_data[field] = 'https://' + url
    
    result['valid'] = len(result['errors']) == 0
    return result