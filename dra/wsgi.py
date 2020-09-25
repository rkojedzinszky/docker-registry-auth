"""
WSGI config for dro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

# re-open sys.stdout to really correspont to FD #1
# Under uwsgi stdout and stderr are all mapped to FD #2
import sys

sys.stdout = open(1, 'w')
sys.__stdout__ = sys.stdout

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dra.settings")

application = get_wsgi_application()
