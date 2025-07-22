"""
Django settings for Research Agent backend project.
"""
import os
from pathlib import Path
import dotenv

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
dotenv.load_dotenv(os.path.join(BASE_DIR, '.env'))

# Security Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-2024-secure-research-agent-django-backend-cybersecurity-intelligence-platform-long-random-key-for-development-only')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'research_agent.apps.ResearchAgentConfig',
]

# Middleware configuration - includes security middleware for both dev and prod
BASE_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Always include for security checks
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    # Development middleware - includes security middleware but with relaxed settings
    MIDDLEWARE = BASE_MIDDLEWARE
else:
    # Production middleware - full security with additional custom middleware
    MIDDLEWARE = [
        'research_agent.security_middleware.SecurityMiddleware',
        'research_agent.security_middleware.EmailSecurityMiddleware', 
        'research_agent.security_middleware.APIKeyAuthMiddleware',
        'django.middleware.security.SecurityMiddleware',
    ] + BASE_MIDDLEWARE

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION = 'backend.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# OpenAI API Key (set this value or use an environment variable for security)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

# Azure OpenAI Configuration
AZURE_EXISTING_AIPROJECT_ENDPOINT = os.environ.get('AZURE_EXISTING_AIPROJECT_ENDPOINT', '')

# Allow requests from your React frontend (ports 3000-3005)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # React app port 3000
    'http://127.0.0.1:3000',  # Alternative localhost for port 3000
    'http://localhost:3001',  # React app port 3001
    'http://127.0.0.1:3001',  # Alternative localhost for port 3001
    'http://localhost:3002',  # React app port 3002
    'http://127.0.0.1:3002',  # Alternative localhost for port 3002
    'http://localhost:3003',  # React app port 3003
    'http://127.0.0.1:3003',  # Alternative localhost for port 3003
    'http://localhost:3004',  # React app port 3004
    'http://127.0.0.1:3004',  # Alternative localhost for port 3004
    'http://localhost:3005',  # React app port 3005
    'http://127.0.0.1:3005',  # Alternative localhost for port 3005
]

# Additional CORS settings for development
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True  # Temporarily enabled for debugging

# Allow specific headers
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Allow specific methods
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Email Configuration
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@example.com')

# File Storage for Reports
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
REPORTS_DIR = os.path.join(MEDIA_ROOT, 'reports')

# Ensure reports directory exists
os.makedirs(REPORTS_DIR, exist_ok=True)

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# Development-friendly security settings
if DEBUG:
    # For development, set minimal security to avoid warnings but keep functionality
    SECURE_HSTS_SECONDS = 0
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    # Note: These are disabled for HTTP development server
    print("🔧 Development mode: Security settings configured for HTTP localhost")
else:
    # Production security settings - enable when deploying with HTTPS
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    print("🔒 Production mode: Full security settings enabled")