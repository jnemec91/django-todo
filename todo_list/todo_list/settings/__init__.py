import os

if os.environ.get('DJANGO_ENV') == 'production':
    print("Running project in production mode")
    from .production import *
else:
    print("Running project in development mode")
    from .development import *