# Student Dashboard

A Django-based student dashboard application.

## Features
- **Authentication**: Login and Signup.
- **Dashboard**:
    - **View Subjects**: Link to Notion page.
    - **Submit Homework**: Upload PDF, select date. Files are uploaded to Google Drive (if configured) or stored locally.
    - **Ask Doubt**: Submit doubts with optional attachments.
    - **View Submitted**: History of submitted homeworks.
- **Audio Feedback**: Plays a sound (`1.mp3`) upon successful homework submission.

## Setup Instructions

1.  **Install Python**: Ensure Python is installed.
2.  **Create Virtual Environment**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate  # Mac/Linux
    ```
3.  **Install Dependencies**:
    ```bash
    pip install django google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```
4.  **Google Drive Setup (Optional)**:
    - Create a Service Account in Google Cloud Console.
    - Download the JSON key file.
    - Rename it to `credentials.json` and place it in the project root (next to `manage.py`).
    - Share the target Google Drive folder with the Service Account email.
5.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```
6.  **Run Server**:
    ```bash
    python manage.py runserver
    ```
7.  **Access**: Open `http://127.0.0.1:8000`.

## Deployment Guide

### Option 1: PythonAnywhere (Recommended for Beginners)
1.  Sign up at [PythonAnywhere](https://www.pythonanywhere.com/).
2.  Go to "Web" tab -> "Add a new web app".
3.  Choose "Django" and your Python version.
4.  Upload your code (zip it or use git).
5.  In the WSGI configuration file, point to your project settings.
6.  Run `pip install -r requirements.txt` in the Bash console.
7.  Reload the web app.

### Option 2: Render.com
1.  Create a `requirements.txt`: `pip freeze > requirements.txt`.
2.  Create a `build.sh` script:
    ```bash
    #!/usr/bin/env bash
    pip install -r requirements.txt
    python manage.py collectstatic --no-input
    python manage.py migrate
    ```
3.  Push code to GitHub.
4.  Connect GitHub repo to Render.
5.  Set "Build Command" to `./build.sh`.
6.  Set "Start Command" to `gunicorn student_dashboard.wsgi:application`.

## Customization
- **Notion Link**: Update the `href` in `templates/dashboard.html`.
- **Audio**: Replace `static/audio/1.mp3` with your desired audio file.
