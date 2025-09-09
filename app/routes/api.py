from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from app.services.resume_parser import ResumeParser
from app.services.template_generator import TemplateGenerator
from app.services.data_processor import DataProcessor
from app.models.resume_model import Resume
from app import db
from app.utils.validators import validate_file
from app.utils.helpers import allowed_file

api_bp = Blueprint('api', __name__)

@api_bp.route('/resume', methods=['POST'])
def create_resume():
    """API endpoint to create resume from raw data"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Process data
        processor = DataProcessor()
        processed_data = processor.process_raw_data(data)
        
        # Save to database
        resume = Resume.from_dict(processed_data)
        db.session.add(resume)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'resume_id': resume.id,
            'message': 'Resume created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/upload', methods=['POST'])
def upload_resume():
    """API endpoint to upload and parse resume file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        template_id = request.form.get('template_id', 'template1')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Validate file
            validation_result = validate_file(file_path)
            if not validation_result['valid']:
                os.remove(file_path)
                return jsonify({'error': validation_result['error']}), 400
            
            # Parse resume
            parser = ResumeParser()
            parsed_data = parser.parse_resume(file_path)
            parsed_data['template_id'] = template_id
            
            # Process data
            processor = DataProcessor()
            processed_data = processor.process_parsed_data(parsed_data)
            
            # Save to database
            resume = Resume.from_dict(processed_data)
            resume.file_path = file_path
            db.session.add(resume)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'resume_id': resume.id,
                'parsed_data': resume.to_dict(),
                'message': 'Resume uploaded and processed successfully'
            }), 201
        else:
            return jsonify({'error': 'Invalid file format'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/resume/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    """Get resume data by ID"""
    try:
        resume = Resume.query.get_or_404(resume_id)
        return jsonify({
            'success': True,
            'data': resume.to_dict()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/resume/<int:resume_id>/html', methods=['GET'])
def get_resume_html(resume_id):
    """Get resume HTML by ID"""
    try:
        resume = Resume.query.get_or_404(resume_id)
        generator = TemplateGenerator()
        resume_html = generator.generate_resume(resume.to_dict())
        
        return jsonify({
            'success': True,
            'html': resume_html
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/resumes', methods=['GET'])
def list_all_resumes():
    """List all resumes"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        resumes = Resume.query.order_by(Resume.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [resume.to_dict() for resume in resumes.items],
            'pagination': {
                'page': page,
                'pages': resumes.pages,
                'per_page': per_page,
                'total': resumes.total
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/resume/<int:resume_id>', methods=['PUT'])
def update_resume(resume_id):
    """Update resume data"""
    try:
        resume = Resume.query.get_or_404(resume_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Process updated data
        processor = DataProcessor()
        processed_data = processor.process_raw_data(data)
        
        # Update resume
        for key, value in processed_data.items():
            if hasattr(resume, key):
                setattr(resume, key, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': resume.to_dict(),
            'message': 'Resume updated successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/resume/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    """Delete resume"""
    try:
        resume = Resume.query.get_or_404(resume_id)
        
        # Delete associated file if exists
        if resume.file_path and os.path.exists(resume.file_path):
            os.remove(resume.file_path)
        
        db.session.delete(resume)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Resume deleted successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500