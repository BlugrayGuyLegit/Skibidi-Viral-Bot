import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials

# Configuration
API_KEY = os.getenv('API_KEY')
CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
CHANNEL_ID = os.getenv('CHANNEL_ID')
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server()
    print('Authentication successful!')

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def upload_video(youtube, file_path, title, description):
    request = youtube.videos().insert(
        part='snippet,status',
        body={
            'snippet': {
                'categoryId': '22',
                'title': title,
                'description': description
            },
            'status': {
                'privacyStatus': 'unlisted'
            }
        },
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )

    response = request.execute()
    print('Video upload successful!')
    return response

def main():
    youtube = get_authenticated_service()
    
    file_path = 'path_to_your_video_file.mp4'  # Replace with the path to your video file
    title = 'My Test Video'
    description = 'This is a test video uploaded from Python script.'

    upload_response = upload_video(youtube, file_path, title, description)
    print('Video ID:', upload_response['id'])

if __name__ == '__main__':
    main()
