# PROJECT_NAME should be changed to Django settings module
import sys, os

sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = "PROJECT_NAME.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

