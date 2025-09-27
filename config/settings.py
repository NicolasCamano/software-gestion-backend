# config/settings.py

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# --- CONFIGURACIONES DE SEGURIDAD PARA PRODUCCIÓN ---

# La SECRET_KEY se leerá de una variable de entorno en Render.
# Si no la encuentra, usa una clave simple (SOLO para desarrollo local).
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-for-development')

# El modo DEBUG será 'False' en producción para mayor seguridad.
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS le dice a Django qué dominios pueden servir la aplicación.
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Esta línea permite que 'localhost' (127.0.0.1) funcione en desarrollo.
if not DEBUG:
    ALLOWED_HOSTS.append('127.0.0.1')


# --- APLICACIONES INSTALADAS ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Necesario para Whitenoise
    'django.contrib.staticfiles',

    # Apps de Terceros
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',

    # Nuestras Apps
    'gestion',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Middleware de Whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Middleware de CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# --- CONFIGURACIÓN DE LA BASE DE DATOS ---

# En producción, usará la URL de la base de datos de Render.


# En desarrollo, creará un archivo db.sqlite3 local.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}


# --- VALIDACIÓN DE CONTRASEÑAS ---

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# --- INTERNACIONALIZACIÓN ---

LANGUAGE_CODE = 'es-ar' # Español de Argentina
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True


# --- ARCHIVOS ESTÁTICOS (PARA EL ADMIN DE DJANGO) ---

STATIC_URL = '/static/'
# En producción (cuando DEBUG es False), los archivos estáticos se guardarán en esta carpeta.
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- CONFIGURACIÓN POR DEFECTO ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- CONFIGURACIONES DE DJANGO REST FRAMEWORK Y CORS ---

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# --- ¡LA CORRECCIÓN FINAL DE CORS ESTÁ AQUÍ! ---

# Primero, definimos la lista de orígenes permitidos que ya teníamos
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    # Asegúrate de que tu URL de Vercel esté aquí y bien escrita
    'https://software-gestion-frontend.vercel.app', 
]

# Como método extra de seguridad y para entornos como Render,
# podemos usar CORS_TRUSTED_ORIGINS. Esto es especialmente útil
# para asegurar que las peticiones 'preflight' funcionen correctamente.
CORS_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    # Añadimos la URL de Vercel aquí también
    'https://software-gestion-frontend.vercel.app',
]

# Si estás usando el plan gratuito de Render y el nombre de tu servicio cambia,
# puedes usar una variable de entorno para la URL del frontend.
# RENDER_FRONTEND_URL = os.environ.get('RENDER_FRONTEND_URL')
# if RENDER_FRONTEND_URL:
#     CORS_ALLOWED_ORIGINS.append(RENDER_FRONTEND_URL)
#     CORS_TRUSTED_ORIGINS.append(RENDER_FRONTEND_URL)