import os
import django
import sys

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medshop_pos.settings')
django.setup()

# Import User model
from django.contrib.auth.models import User

print("Creating superuser for Medical Shop POS System")
print("=============================================")

# Default values
username = "admin"
email = "admin@example.com"
password = "adminpassword123"

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f"Superuser '{username}' already exists")
    sys.exit(0)

# Create the superuser
try:
    superuser = User.objects.create_superuser(username=username, email=email, password=password)
    superuser.save()
    print(f"Superuser '{username}' was created successfully with email '{email}'")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password)}")
    print("\nYou can now log in to the admin interface at /admin")
except Exception as e:
    print(f"Error creating superuser: {e}")
    sys.exit(1)