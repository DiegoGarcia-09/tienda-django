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

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    # 1. Cloudinary Storage debe ir ANTES de staticfiles
    'cloudinary_storage', 
    'django.contrib.staticfiles',
    
    # 2. Luego la librería base de Cloudinary
    'cloudinary',
    
    # 3. Tus apps y utilidades
    'django.contrib.humanize',
    'productos',
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


# Reemplaza la sección 10 que te pasé antes por esta:
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.StaticFilesStorage", # Versión más estable para Render
    },
}

# Muy importante para que se armen los links de las fotos
MEDIA_URL = '/media/'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'de0qx1mkm',
    'API_KEY': '943213471526688',
    'API_SECRET': 'Kd4UjJSf8Gz_RscpBhqYiafGH1c'
}