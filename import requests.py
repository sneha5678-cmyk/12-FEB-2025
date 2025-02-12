import requests
import os
from google.colab import files
import json

# Set your API key
API_KEY = "AIzaSyD6L0Uqythnm15X8XRaflLQsuYDXJE1XSE"

# Use provided Channel ID
CHANNEL_ID = "UCnC8SAZzQiBGYVSKZ_S3y4Q"

# Create a folder to store thumbnails
os.makedirs("thumbnails", exist_ok=True)

# Fetch up to 100 latest videos using pagination
max_results = 50  # API limit per request
video_count = 0
next_page_token = ""
thumbnails_downloaded = 0

while thumbnails_downloaded < 100 and next_page_token is not None:
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&type=video&maxResults={max_results}&pageToken={next_page_token}"
    response = requests.get(url)
    data = response.json()
    
    # Print response for debugging
    print(json.dumps(data, indent=2))
    
    if "items" not in data:
        break
    
    # Extract and download thumbnails
    for item in data["items"]:
        if "snippet" in item:
            video_id = item["id"].get("videoId")
            if video_id:
                thumbnail_url = item["snippet"]["thumbnails"].get("high", {}).get("url")
                if thumbnail_url:
                    print(f"Downloading: {thumbnail_url}")
                    
                    # Download and save the thumbnail
                    img_data = requests.get(thumbnail_url).content
                    with open(f"thumbnails/{video_id}.jpg", "wb") as f:
                        f.write(img_data)
                    
                    thumbnails_downloaded += 1
                    if thumbnails_downloaded >= 100:
                        break
    
    # Get next page token if exists
    next_page_token = data.get("nextPageToken") if "nextPageToken" in data else None
    if not next_page_token:
        break

# Zip the thumbnails for easy download
!zip -r thumbnails.zip thumbnails

# Provide download link
files.download("thumbnails.zip")

print(f"Thumbnails extracted and downloaded successfully! Total: {thumbnails_downloaded}")
