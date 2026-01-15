import os
from pathlib import Path

# Import base settings
from .settings import *

# Override database to connect to production Cloud SQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'assignment_tracker_db',
        'USER': 'django-user', 
        'PASSWORD': 'Chinnu_Krishna_wrecK_567*',  # Replace with your actual password
        'HOST': '34.93.176.220',  # Your Cloud SQL public IP
        'PORT': '5432',
    }
}

# Keep debug on for local data loading
DEBUG = True

print("🔗 Connected to PRODUCTION Cloud SQL database!")
print("🚨 WARNING: You are loading data directly to production!")