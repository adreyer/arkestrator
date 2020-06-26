import django.core.wsgi
import sys

sys.path.append("/opt/arkestrator/virtualenv/src/arkestrator")
sys.path.append("/opt/arkestrator/virtualenv/src/arkestrator/arkestrator")
sys.path.append("/opt/arkestrator/arkestrator_settings")


application = django.core.wsgi.get_wsgi_application()
