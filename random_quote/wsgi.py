"""
WSGI config for random_quote project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

project_home = '/home/Lew77795/random-quote-test'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

venv_path = '/home/Lew77795/random_quote/venv'
activate_env = os.path.join(venv_path, 'bin/activate_this.py')
with open(activate_env) as f:
    exec(f.read(), {'__file__': activate_env})

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'random_quote.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
