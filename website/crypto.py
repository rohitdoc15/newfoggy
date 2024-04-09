import os
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd

def format_publish_date(date_str):
    # Parse the original date string
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    # Format it to a simpler format, e.g., "YYYY-MM-DD HH:MM:SS"
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")

def youtube_search(api_key, query, max_results=500):
    # Set up the YouTube API client
    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey=api_key)

    # Calculate the date 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat() + 'Z'

    # Create lists to store data
    titles = []
    channels = []
    publish_dates = []
    video_links = []

    # Perform the search
    next_page_token = None
    total_results = 0

    while total_results < max_results:
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=min(50, max_results - total_results),
            pageToken=next_page_token,
            publishedAfter=seven_days_ago
        )
        response = request.execute()

        # Extract video details
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            channel_name = item["snippet"]["channelTitle"]
            publish_date = format_publish_date(item["snippet"]["publishedAt"])
            video_id = item["id"]["videoId"]
            video_link = f"https://www.youtube.com/watch?v={video_id}"

            # Append data to lists
            titles.append(video_title)
            channels.append(channel_name)
            publish_dates.append(publish_date)
            video_links.append(video_link)

            print(f"Title: {video_title}")
            print(f"Channel: {channel_name}")
            print(f"Publish Date: {publish_date}")
            print(f"Video Link: {video_link}")
            print("\n")

        total_results += len(response["items"])
        next_page_token = response.get("nextPageToken")

        # If there are no more pages, break the loop
        if not next_page_token:
            break

    # Create a Pandas DataFrame
    df = pd.DataFrame({
        'Title': titles,
        'Channel': channels,
        'Publish Date': publish_dates,
        'Video Link': video_links
    })

    # Save to Excel file
    df.to_excel('youtube_results.xlsx', index=False)

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = "AIzaSyCj03npWHxB9EN64MqhiuRTOHMQyIWK7DU"
    
    # Enter the search query
    search_query = input("Enter the search query: ")

    # Number of results to fetch (default is 500)
    results_count = int(input("Enter the number of results to fetch (default is 500): ") or 500)

    youtube_search(api_key, search_query, results_count)
