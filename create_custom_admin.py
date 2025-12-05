
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_dashboard.settings')
django.setup()

from django.contrib.auth.models import User

def create_custom_admin():
    username = 'Priyansh'
    password = 'Mgrgta@85'
    email = 'priyansh@example.com' 

    try:
        if User.objects.filter(username=username).exists():
            print(f"User '{username}' already exists. Updating password...")
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f"Password updated for '{username}'.")
        else:
            User.objects.create_superuser(username, email, password)
            print(f"Superuser '{username}' created successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    create_custom_admin()
