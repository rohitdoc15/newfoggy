import sys
sys.path.append('/home/rohit/news/website')

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')  # replace my_project with your project name
django.setup()

from googleapiclient.discovery import build
from pages.models import NewsChannel, Video  # replace your_app_name with the actual name of your Django app
from datetime import datetime, timedelta
from pytz import timezone
# AIzaSyDzQngwEKSXznBCvRoURIXs4-WZeps4uHA
# AIzaSyCj03npWHxB9EN64MqhiuRTOHMQyIWK7DU
api_key = "AIzaSyDzQngwEKSXznBCvRoURIXs4-WZeps4uHA"
youtube = build('youtube', 'v3', developerKey=api_key)

def update(channel):
    channel_id = channel.channel_id
    local_tz = timezone('Asia/Kolkata')  # Replace 'YOUR_LOCAL_TIMEZONE' with your local timezone
    now = datetime.now(local_tz)
    time_24_hours_ago = now - timedelta(hours=24)
    today = time_24_hours_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
    tomorrow = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    request = youtube.search().list(part="snippet", channelId=channel_id, order='date', maxResults=200, publishedAfter=today, publishedBefore=tomorrow)
    response = request.execute()

    videos_last_24_hours = []
    for item in response['items']:
        if item['id']['kind'] == "youtube#video":
            videos_last_24_hours.append(item['snippet']['title'])
            
            thumbnail_url = item['snippet']['thumbnails']['default']['url']
            hq_thumbnail_url = thumbnail_url.replace('/default.jpg', '/hqdefault.jpg')
            
            video, created = Video.objects.get_or_create(
                channel=channel,
                title=item['snippet']['title'],
                video_url=f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                defaults={
                    'thumbnail_url': hq_thumbnail_url,
                    'published_date': item['snippet']['publishedAt'],
                    # Add additional fields as necessary
                } 
            )
            
    # Print the number of videos for the channel
    print(f"Channel: {channel.name}, Videos: {len(videos_last_24_hours)}")

    # Print the titles of videos from the last 24 hours
    print("Titles of videos from the last 24 hours:")
    for title in videos_last_24_hours:
        print(title)


news_channels = NewsChannel.objects.all()

for channel in news_channels:
    try:
        update(channel)
    except Exception as e:
        print('Error in', channel.name, e)