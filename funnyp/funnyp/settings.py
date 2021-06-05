import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'r82e(w@m#9*_8=__$n&m8&e1vh7c*@g5ff1#@(*+6gpbwa6^m9'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django_resized',
    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    'posts.apps.PostsConfig',
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'livereload',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livereload.middleware.LiveReloadScript',
]

ROOT_URLCONF = 'funnyp.urls'

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
                'funnyp.context_processors.popularposts',
                'funnyp.context_processors.userframe',
                
            ],
        },
    },
]

WSGI_APPLICATION = 'funnyp.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

CKEDITOR_UPLOAD_PATH = 'posts_picall'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'default',
        'toolbarCanCollapse' : 'true',
        'width': 'auto',
        'height': 700,
        'toolbar_default': [
            ['Preview', '-', 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 
            'Undo', 'Redo', '-', 
            'Find', 'Change', 'Scayt', '-', 
            'Link', 'Unlink', 'Anchor', '-',], '/',
            [ 'Styles', 'Format', 'Font', 'FontSize', '-',
            'Image', 'Table', 'HorizontalRule', 'SpecialChar', 'Smiley', 'SpecialChar', '-', 
            'Maximize'], '/',
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 
            'CopyFormatting', 'RemoveFormat', '-', 'NumberedList', 'BulletedList', '-', 
            'Outdent', 'Indent', '-', 
            'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 
            'BidiLtr', 'BidiRtl', 'Language', 'About']
        ]
    },
}

LANGUAGE_CODE = 'pl'
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGIN_REDIRECT_URL = 'blog-home'
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')