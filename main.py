import logging
import os

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src import database, frigate_api, google_drive

load_dotenv()

FRIGATE_URL = os.getenv('FRIGATE_URL', 'http://192.168.123.100:5000')
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE', 'credentials/google_drive_credentials.json')
TOKEN_FILE = os.getenv('TOKEN_FILE', 'credentials/token.json')
SCOPES = ['https://www.googleapis.com/auth/drive']
DAYS = int(os.getenv('DAYS', 3))  # Standardwert ist 3, falls nicht in der .env Datei definiert

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('logs/app.log'),
                        logging.StreamHandler()
                    ])


def create_service():
    """Create and return a Google Drive service client."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)


def main():
    """Main function to initialize services and process events."""
    logging.info("Initializing Google Drive Service...")
    service = create_service()

    logging.info("Initializing database...")
    database.init_db()

    days = DAYS if DAYS != -1 else None  # -1 means fetch all events
    logging.info(f"Fetching events from {FRIGATE_URL} with days={days}...")
    events = frigate_api.fetch_events(FRIGATE_URL, days=days)
    for event in events:
        event_id = event.get('id', 'Unknown')
        video_url = frigate_api.generate_video_url(FRIGATE_URL, event_id)
        logging.info(f"Processing event {event_id} with video URL {video_url}")
        if database.event_uploaded(event_id):
            logging.info(f"Event {event_id} already uploaded.")
            continue
        if google_drive.upload_to_google_drive(service, event, FRIGATE_URL):
            database.insert_event(event_id, True)
            logging.info(f"Event {event_id} successfully uploaded to Google Drive.")
        else:
            logging.error(f"Error uploading event {event_id}.")


if __name__ == "__main__":
    main()
