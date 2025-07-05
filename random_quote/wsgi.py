"""
WSGI config for random_quote project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

project_path = '/home/Lew77795/random-quote-test'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'random_quote.settings'

# activate_this = '/home/Lew77795/.virtualenvs/.venv/bin/activate_this.py'
# exec(open(activate_this).read(), {'__file__': activate_this})

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
