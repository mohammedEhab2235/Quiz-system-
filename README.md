# Django Quiz System

A comprehensive web-based examination and quiz management system built with Django, featuring National ID authentication, interface-based access control, and advanced reporting capabilities.

## Features

### Core Functionality
- **National ID Authentication**: Secure login system using Egyptian National ID format
- **Multi-Role Access Control**: Interface-based permissions for different user types
- **Exam Management**: Create, edit, and manage multiple-choice and true/false questions
- **Auto-Save & Session Recovery**: Automatic saving of exam progress with session recovery
- **Real-time Progress Tracking**: Live progress bars and completion status
- **Comprehensive Reporting**: Detailed analytics and performance reports

### Administrative Features
- **User Management**: Complete CRUD operations for user accounts
- **Course & Exam Creation**: Intuitive interfaces for content management
- **Question Bank**: Organized question management with multiple question types
- **Assignment System**: Flexible exam assignment to users and groups
- **Bulk Operations**: Mass user management and interface access control

### Reporting & Analytics
- **User History Tracking**: Complete audit trail of user activities
- **Performance Analytics**: Detailed score analysis and statistics
- **Export Capabilities**: Excel and PDF export for reports and user data
- **Progress Visualization**: Interactive charts and progress indicators

### Technical Features
- **Responsive Design**: Mobile-friendly Bootstrap-based UI
- **Database Flexibility**: SQLite default with SQL Server support
- **Session Management**: Secure session handling with auto-recovery
- **Template System**: Modular Django templates with reusable components

## Technology Stack

- **Backend**: Django 5.1.4
- **Database**: SQLite (default) / SQL Server (configurable)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Custom National ID backend
- **Export Libraries**: openpyxl (Excel), reportlab (PDF)
- **Additional**: Django template tags, custom filters

## Project Structure

```
system/
├── administration/          # Admin interface app
│   ├── models.py           # Core data models
│   ├── views.py            # Admin views and logic
│   ├── urls.py             # Admin URL patterns
│   └── templatetags/       # Custom template tags
├── authentication/         # Authentication system
│   ├── backends.py         # National ID auth backend
│   ├── models.py           # User models
│   ├── views.py            # Auth views
│   └── middleware.py       # Custom middleware
├── exams/                  # Exam taking system
│   ├── models.py           # Exam-related models
│   ├── views.py            # Exam logic
│   └── templatetags/       # Exam filters
├── templates/              # HTML templates
│   ├── administration/    # Admin templates
│   ├── authentication/    # Auth templates
│   ├── exams/             # Exam templates
│   └── base/              # Base templates
├── quiz_system/           # Django project settings
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd system
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/administration/
   - Django admin: http://127.0.0.1:8000/admin/

## Configuration

### Database Configuration

**SQLite (Default)**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**SQL Server (Optional)**
```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'your_server',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}
```

### Authentication Settings

The system uses a custom National ID authentication backend:

```python
AUTHENTICATION_BACKENDS = [
    'authentication.backends.NationalIDBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

## Usage Guide

### For Administrators

1. **User Management**
   - Navigate to `/administration/users/`
   - Create, edit, or delete user accounts
   - Assign interface access permissions

2. **Course & Exam Creation**
   - Create courses at `/administration/courses/`
   - Add exams and questions
   - Configure exam settings (time limits, passing scores)

3. **Question Management**
   - Access question bank at `/administration/questions/`
   - Create multiple-choice and true/false questions
   - Organize questions by course/topic

4. **Assignment & Access Control**
   - Assign exams to users at `/administration/assignments/`
   - Manage interface access permissions
   - Bulk operations for multiple users

5. **Reports & Analytics**
   - View comprehensive reports at `/administration/reports/`
   - Export data in Excel or PDF format
   - Track user performance and progress

### For Exam Takers

1. **Login**
   - Use National ID and password to login
   - Access assigned exams from dashboard

2. **Taking Exams**
   - Navigate through questions using next/previous buttons
   - Answers are auto-saved every 30 seconds
   - Submit exam when completed

3. **View Results**
   - Check exam results and scores
   - Review performance history
   - Download certificates (if available)

## Data Models

### Core Models

- **User**: Extended Django user with National ID
- **Course**: Course information and metadata
- **Exam**: Exam configuration and settings
- **Question**: Question content and options
- **UserExam**: User exam attempts and scores
- **ExamSession**: Session management for exam recovery
- **Interface**: Access control interfaces
- **UserHistory**: Comprehensive activity logging

### Key Relationships

- Users can be assigned to multiple exams
- Exams belong to courses and contain multiple questions
- Questions can be multiple-choice or true/false
- User exam sessions track progress and allow recovery
- Interface access controls user permissions

## API Endpoints

### Authentication
- `POST /auth/login/` - User login
- `POST /auth/logout/` - User logout
- `GET /auth/profile/` - User profile

### Administration
- `GET /administration/users/` - User management
- `GET /administration/courses/` - Course management
- `GET /administration/exams/` - Exam management
- `GET /administration/questions/` - Question management
- `GET /administration/reports/` - Reports and analytics

### Exams
- `GET /exams/` - Available exams
- `GET /exams/<id>/take/` - Take exam
- `POST /exams/<id>/submit/` - Submit exam
- `GET /exams/results/` - Exam results

## Security Features

- **National ID Validation**: Egyptian National ID format validation
- **Session Security**: Secure session management with timeout
- **CSRF Protection**: Built-in Django CSRF protection
- **SQL Injection Prevention**: Django ORM protection
- **XSS Prevention**: Template auto-escaping
- **Access Control**: Interface-based permission system

## Export Features

### Excel Export
- User history data with filtering options
- Comprehensive reports with charts
- Exam results and statistics

### PDF Export
- Formatted reports with professional layout
- User certificates and transcripts
- Performance summaries

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check database configuration in settings.py
   - Ensure database server is running
   - Verify connection credentials

2. **Migration Issues**
   ```bash
   python manage.py makemigrations --empty appname
   python manage.py migrate --fake-initial
   ```

3. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic
   ```

4. **Permission Denied Errors**
   - Check file permissions
   - Ensure proper virtual environment activation

### Debug Mode

For development, ensure `DEBUG = True` in settings.py. For production, set `DEBUG = False` and configure proper error handling.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation for common solutions

## Changelog

### Version 1.0.0
- Initial release
- National ID authentication system
- Complete exam management
- Reporting and analytics
- Export functionality
- Interface-based access control

---

**Note**: This system is designed for educational institutions and organizations requiring secure, scalable examination management with comprehensive reporting capabilities.
