import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/drive.file']
# Using absolute path to avoid any ambiguity
SERVICE_ACCOUNT_FILE = r'C:\Users\HP\Desktop\Student Dashboard\credentials.json'

def upload_to_drive(file_path, file_name):
    """
    Uploads a file to Google Drive using Service Account.
    Returns the webViewLink of the uploaded file.
    """
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"DEBUG: Looking for credentials at: {SERVICE_ACCOUNT_FILE}")
        print(f"DEBUG: Current working dir: {os.getcwd()}")
        print("Warning: credentials.json not found. Skipping GDrive upload.")
        return None

    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': file_name,
            'parents': ['1H8nzhfo_3wsaHaywTn96CXU-JW7zwhm7']
        }
        media = MediaFileUpload(file_path, resumable=True)

        file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        
        return file.get('webViewLink')
    except Exception as e:
        print(f"Error uploading to Drive: {e}")
        return None
