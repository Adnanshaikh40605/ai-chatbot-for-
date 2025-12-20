import os
import django
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def create_adnan():
    User = get_user_model()
    username = 'adnan'
    password = '1234'
    
    # Delete existing user if any
    User.objects.filter(username=username).delete()
    
    # Create superuser
    User.objects.create_superuser(username=username, email='', password=password)
    print(f"SUCCESS: Superuser '{username}' created with password '{password}'")

if __name__ == "__main__":
    try:
        create_adnan()
    except Exception as e:
        print(f"ERROR: {str(e)}")
