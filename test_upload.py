import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Hardcoded for testing
SERVICE_ACCOUNT_FILE = r'C:\Users\HP\Desktop\Student Dashboard\credentials.json'
FOLDER_ID = '1H8nzhfo_3wsaHaywTn96CXU-JW7zwhm7'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def test_upload():
    print(f"Testing connectivity...")
    
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print("ERROR: Credentials file not found!")
        return

    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)

        # 0. Verify Identity
        print("\nStep 0: Verifying Identity...")
        about = service.about().get(fields="user").execute()
        email = about['user']['emailAddress']
        print(f"Authenticated as: {email}")
        
        # 1. Check Folder Access (with supportsAllDrives)
        print(f"\nStep 1: Checking Folder Access for ID: {FOLDER_ID}")
        try:
            folder = service.files().get(
                fileId=FOLDER_ID, 
                fields='name, capabilities',
                supportsAllDrives=True
            ).execute()
            print(f"Success! Found folder: '{folder.get('name')}'")
        except Exception as e:
            print(f"Failed to access folder: {e}")

        # List all files (just to see what is visible)
        print("\nListing ALL visible files (first 10):")
        results = service.files().list(
            pageSize=10, 
            fields="files(id, name, owners)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        items = results.get('files', [])

        if not items:
            print('No files found at all.')
        else:
            for item in items:
                print(f"- {item['name']} ({item['id']})")

    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == '__main__':
    test_upload()
