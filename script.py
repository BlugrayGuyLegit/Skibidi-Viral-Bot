import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

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
    
def search_videos(query, max_results=5):
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        order='viewCount',
        maxResults=max_results
    )
    response = request.execute()
    return response['items']

# Recherche de vidéos
videos = search_videos('Skibidi Toilet')
for video in videos:
    video_id = video['id']['videoId']
    title = video['snippet']['title']
    description = f"Original video by {video['snippet']['channelTitle']}.\n\n" \
                  f"Watch the original here: https://www.youtube.com/watch?v={video_id}"
    
    # Supposons que la vidéo est déjà téléchargée dans 'video.mp4'
    with open('video_to_upload.txt', 'w') as file:
        file.write(f"{title}\n{description}\nvideo.mp4")
