import os
import dj_database_url
from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api

# 1. RUTAS BÁSICAS
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. SEGURIDAD
SECRET_KEY = 'django-insecure-x@dqlo-vo9c*$(!(5uz(&5d3nv1wk7ahylwqf-n84ou+1(ck65'
DEBUG = False

# 3. CONFIGURACIÓN DE NGROK Y HOSTS
# El '*' permite que cualquier dirección (incluyendo ngrok) se conecte
ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost']

# 4. APLICACIONES
INSTALLED_APPS += [
    'cloudinary',
    'cloudinary_storage',
    'productos', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # Vital para el formato de precios
    
]

# 5. MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'tienda.urls'

# 6. TEMPLATES
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
                'django.template.context_processors.media',
                'productos.context_processors.carrito_contador',
            ],
        },
    },
]

WSGI_APPLICATION = 'tienda.wsgi.application'

# 7. BASE DE DATOS
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}

# 8. IDIOMA Y HORA
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# 9. ARCHIVOS ESTÁTICOS Y MULTIMEDIA
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 10. SEGURIDAD EXTRA PARA NGROK (CSRF)
# Esto evita el error 403 al agregar productos al carrito desde ngrok
CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.app',
    'https://*.ngrok.io'
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'diegofdogarcia01@gmail.com' # El correo de tu tienda
EMAIL_HOST_PASSWORD = 'fsgx iymt hbiw ffui' # No es tu clave normal

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'de0qx1mkm',
    'API_KEY': '913189987215356',
    'API_SECRET': 'iHLj9fFNoYatHhHJSkOi8IfjYzY',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'