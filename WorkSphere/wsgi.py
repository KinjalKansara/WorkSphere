# """
# WSGI config for WorkSphere project.

# It exposes the WSGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
# """

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WorkSphere.settings')

# application = get_wsgi_application()


import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Define BASE_DIR manually
BASE_DIR = Path(__file__).resolve().parent.parent

# Ensure the project directory is in the system path
sys.path.append(str(BASE_DIR))

# Load environment variables
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WorkSphere.settings')

# Get WSGI application
application = get_wsgi_application()

