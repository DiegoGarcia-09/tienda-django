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

# 3. CONFIGURACIÓN DE HOSTS
ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost', 'tienda-django-mgsu.onrender.com']

# 4. APLICACIONES
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    # Cloudinary Storage debe ir ANTES de staticfiles para tomar el control
    'cloudinary_storage', 
    'django.contrib.staticfiles',
    
    'cloudinary',
    'django.contrib.humanize',
    'productos',
]

# 5. MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Para servir estáticos en Render
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
                'django.template.context_processors.media', # Necesario para las fotos
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

# URL para acceder a los archivos multimedia (Cloudinary)
MEDIA_URL = '/media/'

# 10. CONFIGURACIÓN DE ALMACENAMIENTO (STORAGES)
# Esta configuración permite que los archivos estáticos los maneje WhiteNoise 
# y las imágenes las maneje Cloudinary
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# 11. CREDENCIALES DE CLOUDINARY
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'de0qx1mkm',
    'API_KEY': '943213471526688',
    'API_SECRET': 'Kd4UjJSf8Gz_RscpBhqYiafGH1c'
}

# 12. SEGURIDAD EXTRA Y CORREO
CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.app',
    'https://*.ngrok.io',
    'https://tienda-django-mgsu.onrender.com'
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'diegofdogarcia01@gmail.com'
EMAIL_HOST_PASSWORD = 'fsgx iymt hbiw ffui'