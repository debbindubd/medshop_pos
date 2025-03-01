import os
import sys
import subprocess

# This script runs Django migrations for the Medical Shop POS application
print("Running Django migrations for Medical Shop POS")
print("============================================")

# Run makemigrations
print("\nRunning makemigrations...")
try:
    result = subprocess.run([sys.executable, "manage.py", "makemigrations", "pos"], 
                         capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)
except Exception as e:
    print(f"Error during makemigrations: {e}")
    sys.exit(1)

# Run migrations
print("\nRunning migrations...")
try:
    result = subprocess.run([sys.executable, "manage.py", "migrate"], 
                         capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)
except Exception as e:
    print(f"Error during migrations: {e}")
    sys.exit(1)

print("\nMigrations completed successfully!")
print("You can now run 'python create_superuser.py' to create an admin user")