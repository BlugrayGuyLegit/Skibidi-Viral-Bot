import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials

# Configuration
API_KEY = os.getenv('API_KEY')
CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Authentification
credentials = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRETS_FILE, SCOPES)
youtube = build('youtube', 'v3', developerKey=API_KEY, credentials=credentials)

def upload_video(file_path, title, description):
    media = MediaFileUpload(file_path, mimetype='video/*', resumable=True)
    request = youtube.videos().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['Skibidi Toilet', 'Buzz'],
            },
            'status': {
                'privacyStatus': 'public'
            }
        },
        media_body=media
    )
    response = request.execute()
    return response

# Lire les informations de la vidéo à partir du fichier
with open('video_to_upload.txt', 'r') as file:
    title = file.readline().strip()
    description = file.readline().strip()
    file_path = file.readline().strip()

upload_response = upload_video(file_path, title, description)
new_video_id = upload_response['id']

# Réponse aux commentaires sur la nouvelle vidéo
def respond_to_comments(video_id, response_text):
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText'
    )
    response = request.execute()
    comments = response.get('items', [])
    
    for comment in comments:
        comment_id = comment['id']
        reply_request = youtube.comments().insert(
            part='snippet',
            body={
                'snippet': {
                    'parentId': comment_id,
                    'textOriginal': response_text
                }
            }
        )
        reply_request.execute()

respond_to_comments(new_video_id, "Thank you for watching!")
