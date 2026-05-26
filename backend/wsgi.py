import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# 🟢 FORCE AUTOMATIC MIGRATIONS ON SERVER START
try:
    import django
    django.setup()
    from django.core.management import call_command
    print("Running database migrations...")
    call_command('migrate', interactive=False)
    print("Database migrations applied successfully!")
except Exception as e:
    print(f"Migration auto-run failed: {e}")

application = get_wsgi_application()