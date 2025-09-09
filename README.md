# Resume Generator

A Flask-based resume generator application that allows users to create professional resumes from raw data or by uploading existing resume files. The application uses AI/ML transformers to parse and enhance resume content, then generates beautiful resumes using customizable templates.

## Features

- **Two Input Methods**:
  - Create resume from scratch using a comprehensive form
  - Upload existing resume files (PDF, DOCX, DOC, TXT) for parsing and enhancement

- **AI-Powered Processing**:
  - Intelligent resume parsing using transformers
  - Content enhancement and formatting
  - Skills categorization and experience optimization

- **Multiple Templates**:
  - Professional Template (Traditional, corporate-friendly)
  - Modern Template (Contemporary design with gradients)
  - Creative Template (Eye-catching design for creative professionals)

- **Database Storage**:
  - Save and manage multiple resumes
  - Version tracking with timestamps
  - Easy retrieval and editing

- **Production Ready**:
  - Dockerized application
  - Comprehensive error handling
  - Input validation and security measures
  - RESTful API endpoints

## Project Structure

```
resume_app/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── resume_model.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── api.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── resume_parser.py
│   │   ├── template_generator.py
│   │   └── data_processor.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── uploads/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── raw_data_form.html
│   │   ├── upload_form.html
│   │   └── resume_templates/
│   │       ├── template1.html
│   │       ├── template2.html
│   │       └── template3.html
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
│   ├── test_services.py
│   └── test_models.py
├── migrations/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── run.py
└── wsgi.py
```

## Installation & Setup

### Prerequisites

- Python 3.9+
- pip
- Docker (optional, for containerized deployment)

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd resume_app
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application**:
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:5000`

### Docker Setup

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **Or build and run manually**:
   ```bash
   docker build -t resume-generator .
   docker run -p 5000:5000 resume-generator
   ```

## Usage

### Creating a Resume from Scratch

1. Navigate to the home page
2. Click "Start Creating" or go to `/raw-data`
3. Fill in the comprehensive form with your information:
   - Personal details (name, email, phone, etc.)
   - Professional summary
   - Work experience
   - Education
   - Skills
   - Projects
   - Certifications
4. Select a template
5. Click "Generate Resume"

### Uploading an Existing Resume

1. Navigate to the home page
2. Click "Upload Resume" or go to `/upload`
3. Select your resume file (PDF, DOCX, DOC, or TXT)
4. Choose an output template
5. Configure processing options
6. Click "Process & Generate Resume"

### Managing Resumes

- View all your resumes at `/resumes`
- Click on any resume to view or edit
- Delete or duplicate resumes as needed

## API Endpoints

The application provides RESTful API endpoints:

### Resume Management
- `POST /api/resume` - Create new resume from JSON data
- `GET /api/resume/<id>` - Get resume data by ID
- `PUT /api/resume/<id>` - Update existing resume
- `DELETE /api/resume/<id>` - Delete resume
- `GET /api/resumes` - List all resumes (paginated)

### File Upload
- `POST /api/upload` - Upload and parse resume file

### Resume Generation
- `GET /api/resume/<id>/html` - Get generated HTML for resume

## Configuration

Key configuration options in `.env`:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///resume_app.db
UPLOAD_FOLDER=app/static/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or run individual test files:

```bash
python -m unittest tests.test_routes
python -m unittest tests.test_services
python -m unittest tests.test_models
```

## Architecture

### Services Layer

- **ResumeParser**: Handles file upload and text extraction from various formats
- **DataProcessor**: Cleans, validates, and enhances resume data using AI/ML
- **TemplateGenerator**: Renders resume data into HTML using Jinja2 templates

### Models

- **Resume**: SQLAlchemy model for storing resume data with JSON fields for complex data structures

### Routes

- **Main Routes**: Handle web interface and form processing
- **API Routes**: Provide RESTful endpoints for programmatic access

### Utilities

- **Validators**: Input validation and security checks
- **Helpers**: Common utility functions for file handling, formatting, etc.

## Features in Detail

### AI-Powered Resume Parsing

The application uses transformer models to:
- Extract structured data from unstructured resume text
- Identify and categorize different resume sections
- Enhance job descriptions with action verbs
- Standardize date formats and educational qualifications

### Template System

Three professionally designed templates:

1. **Professional**: Clean, traditional layout suitable for corporate environments
2. **Modern**: Contemporary design with color gradients and modern typography
3. **Creative**: Bold, creative design perfect for design and creative roles

### Security Features

- File upload validation and size limits
- Input sanitization and validation
- SQL injection protection via SQLAlchemy
- XSS protection in templates
- Secure file handling

### Performance Optimizations

- Database indexing on commonly queried fields
- Lazy loading of resume relationships
- Optimized template rendering
- Static file caching

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite to ensure everything passes
5. Commit your changes: `git commit -am 'Add new feature'`
6. Push to the branch: `git push origin feature-name`
7. Create a Pull Request

## Deployment

### Production Deployment with Docker

1. **Build production image**:
   ```bash
   docker build -t resume-generator:production .
   ```

2. **Run with environment variables**:
   ```bash
   docker run -d \
     -p 80:5000 \
     -e FLASK_ENV=production \
     -e SECRET_KEY=your-production-secret \
     -e DATABASE_URL=postgresql://user:pass@host:port/db \
     -v /path/to/uploads:/app/app/static/uploads \
     resume-generator:production
   ```

### Environment Variables for Production

```env
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key
DATABASE_URL=postgresql://user:password@host:port/database
UPLOAD_FOLDER=/app/app/static/uploads
MAX_CONTENT_LENGTH=16777216
```

## Troubleshooting

### Common Issues

1. **File upload errors**: Check file size limits and permissions on upload directory
2. **Template rendering issues**: Ensure all required template variables are provided
3. **Database connection errors**: Verify DATABASE_URL and database server availability
4. **Memory issues with large files**: Adjust MAX_CONTENT_LENGTH and server memory limits

### Logs

Check application logs for detailed error information:
```bash
docker logs <container-name>
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Flask and SQLAlchemy
- Uses Bootstrap for responsive UI
- Powered by Transformers library for AI features
- Font Awesome for icons
