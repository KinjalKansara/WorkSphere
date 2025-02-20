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


from django.core.wsgi import get_wsgi_application 
from pathlib import * 
import os 
from dotenv import load_dotenv 
  
BASE_DIR = Path(__file__).resolve().parent.parent 
load_dotenv(os.path.join(BASE_DIR, ".env"))  # Manually load .env 
  
  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WorkSphere.settings') 
  
application = get_wsgi_application()
