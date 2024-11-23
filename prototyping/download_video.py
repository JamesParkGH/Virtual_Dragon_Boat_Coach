#pip install google-api-python-client
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'capstone_sa.json'
PARENT_FOLDER_ID = "1xB4YS_dX4YwHmzFDu0NpH94Yk4eUf4sSJp6RKA1G02rgfGGiBeSHLKvs9GTmq4zoghR-hfwE"

# Google Drive Authentication
def authenticate():
    # Authenticate with the Google API using a service account
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return creds
    except FileNotFoundError:
        print(f"Error: Service account file '{SERVICE_ACCOUNT_FILE}' not found.")
        raise
    except Exception as e:
        print(f"Error during authentication: {e}")
        raise

def upload_photo(file_path):
    # Upload a photo or video to Google Drive
    try:
        creds = authenticate()
        service = build('drive', 'v3', credentials=creds)

        # Define file metadata and parent folder
        file_metadata = {
            'name': file_path.split("/")[-1],  # Use the file's name from the path
            'parents': [PARENT_FOLDER_ID]  # Upload to the specified folder
        }

        # Use MediaFileUpload to specify the local file path for uploading
        media = MediaFileUpload(file_path, resumable=True)

        # Create and upload the file
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f"File uploaded successfully with file ID: {file.get('id')}")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found. Please check the file path.")
    except HttpError as error:
        print(f"An error occurred during file upload: {error}")
    except Exception as e:
        print(f"Unexpected error during upload: {e}")

def download_video(file_name, output_file_path):
    # Download a video file from Google Drive by file name
    try:
        creds = authenticate()
        service = build('drive', 'v3', credentials=creds)

        # Search for the file by name
        results = service.files().list(q=f"name='{file_name}'", fields="files(id, name)").execute()
        files = results.get('files', [])

        if not files:
            print(f"Error: No file found with the name '{file_name}'. Please verify the name.")
            return

        file_id = files[0]['id']  # Assume the first file with the name is the correct one

        # Request to download the file
        request = service.files().get_media(fileId=file_id)
        with io.FileIO(output_file_path, 'wb') as fh:
            # Use MediaIoBaseDownload to download the file in chunks
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}% complete.")

        print("Download completed successfully.")
    except HttpError as error:
        print(f"An error occurred during file download: {error}")
    except FileNotFoundError:
        print(f"Error: Output file path '{output_file_path}' could not be created.")
    except Exception as e:
        print(f"Unexpected error during download: {e}")