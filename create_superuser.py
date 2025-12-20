import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, '/app')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Delete existing user if any
User.objects.filter(username='adnan').delete()

# Create superuser
User.objects.create_superuser(username='adnan', email='', password='1234')
print("SUCCESS: Superuser 'adnan' created with password '1234'")
