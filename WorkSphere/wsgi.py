"""
WSGI config for WorkSphere project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WorkSphere.settings')

application = get_wsgi_application()


# import os
# import sys
# from pathlib import Path
# from dotenv import load_dotenv
# from django.core.wsgi import get_wsgi_application

# # Determine the base directory (two levels up from this file)
# BASE_DIR = Path(__file__).resolve().parent.parent

# # Add the BASE_DIR to the Python path (this helps PythonAnywhere locate your project)
# if str(BASE_DIR) not in sys.path:
#     sys.path.append(str(BASE_DIR))

# # Define the path to your .env file
# env_file = BASE_DIR / '.env'
# if env_file.exists():
#     load_dotenv(dotenv_path=env_file)
# else:
#     print(f"Warning: .env file not found in {BASE_DIR}", file=sys.stderr)

# # Set the default Django settings module
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WorkSphere.settings')

# # Get the WSGI application
# application = get_wsgi_application()



