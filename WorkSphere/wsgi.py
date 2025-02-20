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

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Ensure the project directory is in the system path
sys.path.append(str(BASE_DIR))

# Load .env file manually
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    print(f"Loading environment variables from: {dotenv_path}")  # Debugging line
    load_dotenv(dotenv_path)
else:
    print("WARNING: .env file not found!")  # Debugging line

# Set the default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WorkSphere.settings')

# Print loaded environment variables for debugging
print("EMAIL_HOST_USER:", os.getenv('EMAIL_HOST_USER'))
print("EMAIL_HOST_PASSWORD:", os.getenv('EMAIL_HOST_PASSWORD'))

# Get the WSGI application
application = get_wsgi_application()


