import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('e:\\AI')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')

# Setup Django
django.setup()

from django.contrib.sessions.models import Session
import json

def check_session():
    sessions = Session.objects.all()
    print(f"Total sessions: {sessions.count()}")
    
    session = Session.objects.first()
    if session:
        session_data = session.get_decoded()
        print(f"Session data: {session_data}")
        print(f"Current business ID in session: {session_data.get('current_business_id', 'Not set')}")
    else:
        print("No sessions found")

if __name__ == "__main__":
    check_session()