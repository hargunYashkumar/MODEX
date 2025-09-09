from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os
from app.services.resume_parser import ResumeParser
from app.services.template_generator import TemplateGenerator
from app.services.data_processor import DataProcessor
from app.models.resume_model import Resume
from app import db
from app.utils.validators import validate_file
from app.utils.helpers import allowed_file

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/raw-data')
def raw_data_form():
    return render_template('raw_data_form.html')

@main_bp.route('/upload')
def upload_form():
    return render_template('upload_form.html')

@main_bp.route('/process-raw-data', methods=['POST'])
def process_raw_data():
    try:
        # Extract form data
        data = {
            'full_name': request.form.get('full_name', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'address': request.form.get('address', ''),
            'linkedin': request.form.get('linkedin', ''),
            'github': request.form.get('github', ''),
            'website': request.form.get('website', ''),
            'summary': request.form.get('summary', ''),
            'template_id': request.form.get('template_id', 'template1')
        }
        
        # Process arrays (experience, education, etc.)
        experience_data = []
        exp_count = len([key for key in request.form.keys() if key.startswith('experience_company_')])
        for i in range(exp_count):
            exp = {
                'company': request.form.get(f'experience_company_{i}', ''),
                'position': request.form.get(f'experience_position_{i}', ''),
                'duration': request.form.get(f'experience_duration_{i}', ''),
                'description': request.form.get(f'experience_description_{i}', '')
            }
            if exp['company']:  # Only add if company is provided
                experience_data.append(exp)
        data['experience'] = experience_data
        
        # Education
        education_data = []
        edu_count = len([key for key in request.form.keys() if key.startswith('education_institution_')])
        for i in range(edu_count):
            edu = {
                'institution': request.form.get(f'education_institution_{i}', ''),
                'degree': request.form.get(f'education_degree_{i}', ''),
                'year': request.form.get(f'education_year_{i}', ''),
                'gpa': request.form.get(f'education_gpa_{i}', '')
            }
            if edu['institution']:
                education_data.append(edu)
        data['education'] = education_data
        
        # Skills
        skills_input = request.form.get('skills', '')
        skills_data = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
        data['skills'] = skills_data
        
        # Projects
        projects_data = []
        proj_count = len([key for key in request.form.keys() if key.startswith('project_name_')])
        for i in range(proj_count):
            proj = {
                'name': request.form.get(f'project_name_{i}', ''),
                'description': request.form.get(f'project_description_{i}', ''),
                'technologies': request.form.get(f'project_technologies_{i}', ''),
                'url': request.form.get(f'project_url_{i}', '')
            }
            if proj['name']:
                projects_data.append(proj)
        data['projects'] = projects_data
        
        # Process data using DataProcessor
        processor = DataProcessor()
        processed_data = processor.process_raw_data(data)
        
        # Save to database
        resume = Resume.from_dict(processed_data)
        db.session.add(resume)
        db.session.commit()
        
        # Generate resume using template
        generator = TemplateGenerator()
        resume_html = generator.generate_resume(resume.to_dict())
        
        flash('Resume created successfully!', 'success')
        return render_template('resume_output.html', resume_html=resume_html, resume_id=resume.id)
        
    except Exception as e:
        flash(f'Error processing data: {str(e)}', 'error')
        return redirect(url_for('main.raw_data_form'))

@main_bp.route('/process-upload', methods=['POST'])
def process_upload():
    try:
        if 'resume_file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('main.upload_form'))
        
        file = request.files['resume_file']
        template_id = request.form.get('template_id', 'template1')
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('main.upload_form'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Validate file
            validation_result = validate_file(file_path)
            if not validation_result['valid']:
                os.remove(file_path)  # Clean up invalid file
                flash(f'Invalid file: {validation_result["error"]}', 'error')
                return redirect(url_for('main.upload_form'))
            
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
            
            # Generate resume
            generator = TemplateGenerator()
            resume_html = generator.generate_resume(resume.to_dict())
            
            flash('Resume uploaded and processed successfully!', 'success')
            return render_template('resume_output.html', resume_html=resume_html, resume_id=resume.id)
        else:
            flash('Invalid file format. Please upload PDF, DOCX, or TXT files.', 'error')
            return redirect(url_for('main.upload_form'))
            
    except Exception as e:
        flash(f'Error processing upload: {str(e)}', 'error')
        return redirect(url_for('main.upload_form'))

@main_bp.route('/resume/<int:resume_id>')
def view_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    generator = TemplateGenerator()
    resume_html = generator.generate_resume(resume.to_dict())
    return render_template('resume_output.html', resume_html=resume_html, resume_id=resume.id)

@main_bp.route('/resumes')
def list_resumes():
    resumes = Resume.query.order_by(Resume.created_at.desc()).all()
    return render_template('resume_list.html', resumes=resumes)