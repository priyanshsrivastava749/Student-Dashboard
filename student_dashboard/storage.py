
import os
import mimetypes
from django.conf import settings
from django.core.files.storage import Storage
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

class GoogleDriveSharedStorage(Storage):
    def __init__(self, **kwargs):
        self.service_account_file = settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE
        self.folder_id = getattr(settings, 'GOOGLE_DRIVE_FOLDER_ID', None)
        self.scopes = ['https://www.googleapis.com/auth/drive']
        self._service = None

    @property
    def service(self):
        if self._service is None:
            creds = service_account.Credentials.from_service_account_file(
                self.service_account_file, scopes=self.scopes)
            self._service = build('drive', 'v3', credentials=creds)
        return self._service

    def _open(self, name, mode='rb'):
        # For simplicity, we won't implement full open support yet, 
        # as the primary goal is upload. 
        # But we can implement it if needed using get_media.
        pass

    def _save(self, name, content):
        # Flatten the name to just the filename to store in the specific folder
        # or keep the structure if we implemented folder creation. 
        # For now, let's put it directly in the folder_id.
        filename = os.path.basename(name)
        
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        media_body = MediaIoBaseUpload(
            content.file, mime_type, resumable=True)

        body = {
            'name': filename,
            'mimeType': mime_type
        }
        
        if self.folder_id:
            body['parents'] = [self.folder_id]

        print(f"Uploading {filename} to Google Drive folder {self.folder_id}...")
        
        file_data = self.service.files().create(
            body=body,
            media_body=media_body,
            fields='id, name, webContentLink, webViewLink',
            supportsAllDrives=True, # Crucial for some shared folder permissions
        ).execute()

        # We return the file ID or path. 
        # Django expects the name relative to the storage. 
        # But for retrieval, we might need the ID. 
        # Let's return the name for now, and rely on exists() to look it up by name if needed.
        # OR better: return the ID? No, Django models store this string.
        # If we store just the filename, we might have collisions.
        # Let's return the filename as is.
        return filename

    def exists(self, name):
        filename = os.path.basename(name)
        query = f"name = '{filename}' and trashed = false"
        if self.folder_id:
            query += f" and '{self.folder_id}' in parents"
            
        results = self.service.files().list(
            q=query, 
            fields="files(id)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        return len(results.get('files', [])) > 0

    def url(self, name):
        filename = os.path.basename(name)
        query = f"name = '{filename}' and trashed = false"
        if self.folder_id:
            query += f" and '{self.folder_id}' in parents"
            
        results = self.service.files().list(
            q=query, 
            fields="files(id, webContentLink)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        
        files = results.get('files', [])
        if files:
            return files[0].get('webContentLink')
        return None
