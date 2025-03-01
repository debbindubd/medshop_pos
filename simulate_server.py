import os
import sys
import subprocess

# This script runs the Django development server
print("Starting Medical Shop POS Development Server")
print("===========================================")
print("Attempting to start development server at http://127.0.0.1:8000/")
print("Quit the server with CTRL-C")

try:
    # Run the Django development server
    subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
except KeyboardInterrupt:
    print("\nStopping development server...")
except Exception as e:
    print(f"\nError starting server: {e}")
    print("\nTry running 'python manage.py runserver' manually")
    sys.exit(1)