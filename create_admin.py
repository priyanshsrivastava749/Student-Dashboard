
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_dashboard.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    username = 'admin'
    password = 'adminpassword123'
    email = 'admin@example.com'

    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists.")
    else:
        User.objects.create_superuser(username, email, password)
        print(f"Superuser '{username}' created successfully.")

if __name__ == '__main__':
    create_admin()
