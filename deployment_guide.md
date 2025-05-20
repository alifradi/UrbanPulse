# UrbanPulse Deployment Guide

This document provides instructions for deploying the UrbanPulse Django website to various hosting platforms, with a focus on free solutions like Netlify, Vercel, or PythonAnywhere.

## Project Structure

The UrbanPulse project is organized as follows:

```
urbanpulse/
├── core/                   # Main application
│   ├── static/             # Static files (CSS, JS, images)
│   ├── templates/          # HTML templates
│   ├── admin.py            # Admin configuration
│   ├── forms.py            # Form definitions
│   ├── models.py           # Database models
│   ├── urls.py             # URL routing
│   └── views.py            # View functions
├── urbanpulse_project/     # Project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── venv/                   # Virtual environment
```

## Deployment Options

### Option 1: Netlify Deployment (Static Frontend Only)

For a static version of the site (without Django backend functionality):

1. **Build the static files**:
   ```bash
   python manage.py collectstatic
   ```

2. **Create a `netlify.toml` file** in the project root:
   ```toml
   [build]
     publish = "staticfiles/"
     command = "echo 'Static files ready'"
   ```

3. **Deploy to Netlify**:
   - Sign up for a Netlify account
   - Connect your GitHub repository
   - Configure the build settings as specified in netlify.toml
   - Deploy the site

Note: This option only deploys the static frontend. Forms and dynamic features will not function without a backend.

### Option 2: PythonAnywhere (Full Django Application)

For a complete deployment with backend functionality:

1. **Sign up for a PythonAnywhere account** (free tier available)

2. **Create a new web app**:
   - Choose "Manual configuration"
   - Select Python 3.8 or newer

3. **Set up a virtual environment**:
   ```bash
   mkvirtualenv --python=python3.8 urbanpulse-env
   pip install -r requirements.txt
   ```

4. **Configure WSGI file**:
   - Edit the WSGI configuration file provided by PythonAnywhere
   - Update the path to your project
   - Set the DJANGO_SETTINGS_MODULE to 'urbanpulse_project.settings'

5. **Configure static files**:
   - In PythonAnywhere dashboard, go to the "Web" tab
   - Add static file mappings:
     - URL: /static/ → Directory: /home/yourusername/urbanpulse/staticfiles/
     - URL: /media/ → Directory: /home/yourusername/urbanpulse/media/

6. **Set up the database**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. **Reload the web app** from the PythonAnywhere dashboard

### Option 3: Heroku Deployment

For a scalable deployment with backend functionality:

1. **Install the Heroku CLI** and log in

2. **Create a `Procfile`** in the project root:
   ```
   web: gunicorn urbanpulse_project.wsgi --log-file -
   ```

3. **Create a `runtime.txt`** file:
   ```
   python-3.9.7
   ```

4. **Add `django-heroku` to requirements.txt** and install it:
   ```bash
   pip install django-heroku gunicorn
   pip freeze > requirements.txt
   ```

5. **Update settings.py** for Heroku:
   ```python
   import django_heroku
   
   # Add at the bottom of the file
   django_heroku.settings(locals())
   ```

6. **Create and configure the Heroku app**:
   ```bash
   heroku create urbanpulse
   heroku config:set SECRET_KEY='your_secret_key'
   heroku config:set DEBUG_VALUE='False'
   ```

7. **Deploy to Heroku**:
   ```bash
   git add .
   git commit -m "Prepare for Heroku deployment"
   git push heroku master
   ```

8. **Run migrations and create superuser**:
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

## Environment Variables

For any deployment, ensure these environment variables are set:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to 'False' for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string (if using external database)

## Post-Deployment Steps

1. **Create a superuser** to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

2. **Add initial content** through the admin panel:
   - Team members
   - Services
   - Testimonials
   - Contributions and collaborations

3. **Test all functionality**:
   - Contact form
   - Interactive features
   - Responsive design on various devices

## Troubleshooting

- **Static files not loading**: Ensure collectstatic has been run and paths are configured correctly
- **Database migration issues**: Check migration files and try running migrations manually
- **500 server errors**: Check the server logs for detailed error messages

## Support

For additional help, refer to the documentation for your chosen hosting platform:

- [Netlify Documentation](https://docs.netlify.com/)
- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Heroku Dev Center](https://devcenter.heroku.com/)
