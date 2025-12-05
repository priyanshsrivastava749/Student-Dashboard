
import os
import django
from django.core.files.base import ContentFile
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_dashboard.settings')
django.setup()

from django.core.files.storage import default_storage

def verify_upload():
    print("Testing Django Storage...")
    content = b"Hello Google Drive from Django!"
    filename = "test_django_upload.txt"
    
    try:
        print(f"Attempting to save {filename}...")
        path = default_storage.save(filename, ContentFile(content))
        print(f"File saved at: {path}")
        
        print("Checking if file exists...")
        if default_storage.exists(path):
            print("File exists!")
            url = default_storage.url(path)
            print(f"File URL: {url}")
        else:
            print("File NOT found after save.")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    verify_upload()
