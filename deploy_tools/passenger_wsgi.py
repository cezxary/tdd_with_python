# PROJECT_NAME should be changed to Django settings module
import sys
import os
from django.core.wsgi import get_wsgi_application

sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = "PROJECT_NAME.settings"

application = get_wsgi_application()
