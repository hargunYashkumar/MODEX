import os
import uuid
from datetime import datetime
from flask import current_app
from typing import List, Dict, Any, Optional

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    if not filename:
        return False
    
    allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'docx', 'doc', 'txt'})
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return file_ext in allowed_extensions

def generate_unique_filename(original_filename: str) -> str:
    """Generate unique filename to prevent conflicts"""
    if not original_filename:
        return f"{uuid.uuid4().hex}.txt"
    
    name, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    
    return f"{name}_{timestamp}_{unique_id}{ext}"

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def clean_html(text: str) -> str:
    """Remove HTML tags from text"""
    import re
    if not text:
        return ""
    
    # Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', text)
    # Remove extra whitespace
    clean_text = ' '.join(clean_text.split())
    return clean_text

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def format_date(date_obj: datetime, format_str: str = "%B %d, %Y") -> str:
    """Format datetime object to string"""
    if not date_obj:
        return ""
    
    return date_obj.strftime(format_str)

def parse_skills_string(skills_str: str) -> List[str]:
    """Parse comma-separated skills string into list"""
    if not skills_str:
        return []
    
    # Split by common delimiters and clean
    skills = []
    for delimiter in [',', ';', '|', '\n']:
        if delimiter in skills_str:
            skills = skills_str.split(delimiter)
            break
    else:
        skills = [skills_str]
    
    # Clean and filter empty skills
    cleaned_skills = []
    for skill in skills:
        skill = skill.strip()
        if skill and skill not in cleaned_skills:
            cleaned_skills.append(skill)
    
    return cleaned_skills

def create_breadcrumb(page_name: str, parent_pages: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, str]]:
    """Create breadcrumb navigation"""
    breadcrumb = [{'name': 'Home', 'url': '/'}]
    
    if parent_pages:
        breadcrumb.extend(parent_pages)
    
    breadcrumb.append({'name': page_name, 'url': ''})
    return breadcrumb

def get_file_icon(filename: str) -> str:
    """Get appropriate icon for file type"""
    if not filename:
        return 'file'
    
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    icon_map = {
        'pdf': 'file-pdf',
        'doc': 'file-word',
        'docx': 'file-word', 
        'txt': 'file-text',
        'rtf': 'file-text'
    }
    
    return icon_map.get(ext, 'file')

def validate_json_structure(data: Any, required_keys: List[str]) -> bool:
    """Validate if JSON data has required structure"""
    if not isinstance(data, dict):
        return False
    
    for key in required_keys:
        if key not in data:
            return False
    
    return True

def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Merge two dictionaries, with dict2 taking precedence"""
    merged = dict1.copy()
    merged.update(dict2)
    return merged

def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """Extract keywords from text"""
    import re
    
    if not text:
        return []
    
    # Remove common stop words
    stop_words = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
        'above', 'below', 'between', 'among', 'around', 'under', 'over', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
        'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
        'this', 'that', 'these', 'those', 'a', 'an'
    }
    
    # Extract words
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    # Filter keywords
    keywords = []
    for word in words:
        if len(word) >= min_length and word not in stop_words:
            if word not in keywords:
                keywords.append(word)
    
    return keywords[:20]  # Limit to top 20 keywords

def paginate_results(items: List, page: int, per_page: int = 10) -> Dict[str, Any]:
    """Paginate a list of items"""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_items = items[start:end]
    
    return {
        'items': paginated_items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page,
        'has_prev': page > 1,
        'has_next': end < total,
        'prev_page': page - 1 if page > 1 else None,
        'next_page': page + 1 if end < total else None
    }

def safe_get(dictionary: Dict, key: str, default: Any = None) -> Any:
    """Safely get value from dictionary with nested key support"""
    keys = key.split('.')
    value = dictionary
    
    try:
        for k in keys:
            value = value[k]
        return value
    except (KeyError, TypeError):
        return default

def format_phone_display(phone: str) -> str:
    """Format phone number for display"""
    if not phone:
        return ""
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    
    return phone  # Return original if can't format