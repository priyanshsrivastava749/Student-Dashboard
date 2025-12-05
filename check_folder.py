
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

SERVICE_ACCOUNT_FILE = r'C:\Users\HP\Desktop\Student Dashboard\credentials.json'
FOLDER_ID = '1H8nzhfo_3wsaHaywTn96CXU-JW7zwhm7'
SCOPES = ['https://www.googleapis.com/auth/drive']

def check_folder_type():
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)

        print(f"Checking folder {FOLDER_ID}...")
        file = service.files().get(
            fileId=FOLDER_ID,
            fields='id, name, driveId, capabilities, owners',
            supportsAllDrives=True
        ).execute()

        print("Folder Metadata:")
        print(f"Name: {file.get('name')}")
        print(f"Drive ID: {file.get('driveId')} (If present, it is in a Shared Drive)")
        print(f"Owners: {file.get('owners')}")
        print(f"Can Add Children: {file.get('capabilities', {}).get('canAddChildren')}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_folder_type()
