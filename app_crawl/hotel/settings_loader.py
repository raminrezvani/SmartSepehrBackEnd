import sys
import os

def load_django_settings():
    # Add the project root to the Python path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.append(project_root)
    
    # Set the Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_providers_api.settings')
    
    # Configure Django settings
    import django
    django.setup()
    
    # Now we can import settings
    from django.conf import settings
    return settings