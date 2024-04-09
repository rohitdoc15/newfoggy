import os
import django
import subprocess
import json
import openai
import re
import random
import urllib.request
import requests
from PIL import Image
from twitter.account import Account
from django.conf import settings

import sys
sys.path.append('/home/rohit/news/website')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from pages.models import GeneratedBlog

openai.api_key = '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'

def get_tweet_data(url):
    result = subprocess.run(['node', 'tweet.js', url], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Node.js subprocess exited with code {result.returncode}, stderr:\n{result.stderr}")
    lines = result.stdout.splitlines()
    json_start_index = next((i for i, line in enumerate(lines) if line.strip().startswith('{') and line.strip().endswith('}')), None)
    if json_start_index is None:
        raise ValueError("No JSON object found in stdout")
    data = json.loads(lines[json_start_index])
    return data

from PIL import Image

from google_images_search import GoogleImagesSearch
import itertools

import shutil
import tempfile


import re

def generate_image_search_query(blog_title):
    model = "gpt-3.5-turbo"

    prompt = f'''
    I have written a blog titled '{blog_title}'. Can you suggest a Google search query to find a suitable image for this blog?
    '''

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a skilled blogger and SEO expert."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=60,
        temperature=0.7
    )

    response_text = response.choices[0].message['content']

    # Extract the text between single quotes
    search_query = re.findall(r'[\'"](.*?)[\'"]', response_text)

    if search_query:
        # If there's a match, return the first group found
        suggested_query = search_query[0]
    else:
        # If no match is found, return the whole response
        suggested_query = response_text

    print(suggested_query)
    return suggested_query



def get_google_image(blog_title):
    # Provide your Google Custom Search API keys and CXs
    query = generate_image_search_query(blog_title)

    api_keys = [
        ('AIzaSyASfWANIMbq1Ta9y8x5DHIbPwOyOawHCsc', 'f4d874a23b5564000'),
        ('AIzaSyCyziO3H25aTxAGzPfLk34q1_gVL6vW62M', '3703ccef476244145'),
        ('AIzaSyCj03npWHxB9EN64MqhiuRTOHMQyIWK7DU', 'f2da21573b2f1485b'),
    ]

    for api_key, cx in api_keys:
        try:
            # Create a new GoogleImagesSearch object with the current API key and CX
            gis = GoogleImagesSearch(api_key, cx)

            truncated_query = ' '.join(query.split()[:5])

            _search_params = {
                'q': query,   # Search query
                'num': 10,    # Number of results to return
                'fileType': 'jpg|png',  # File types to return
            }

            # Search for images
            gis.search(search_params=_search_params)

            # Check if any results were returned
            if gis.results():
                for image in gis.results():
                    # Create a temporary directory and download the image there
                    with tempfile.TemporaryDirectory() as temp_dir:
                        image.download(temp_dir)
                        downloaded_image_path = os.path.join(temp_dir, os.listdir(temp_dir)[0])  # Get the path of the downloaded image

                        # Open the image using PIL
                        img = Image.open(downloaded_image_path)

                        # Check the image's width
                        if img.width >= 800:
                            # Define the image keyword used in the file name
                            safe_image_keywords = ' '.join(re.sub(r'[^\w\s]', '', truncated_query).split()[-4:])

                            # Define paths for the .jpg and .webp files
                            jpg_file_name = f"{safe_image_keywords}.jpg"
                            webp_file_name = f"{safe_image_keywords}.webp"

                            # Define the final paths for the images
                            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get the Django base directory
                            jpg_file_path = os.path.join(base_dir, 'media', jpg_file_name)
                            webp_file_path = os.path.join(base_dir, 'media', webp_file_name)

                            # Ensure the directory exists
                            os.makedirs(os.path.dirname(jpg_file_path), exist_ok=True)

                            # Move the downloaded image to the desired location with the desired name
                            shutil.move(downloaded_image_path, jpg_file_path)

                            # Convert the image to webp
                            img = Image.open(jpg_file_path)
                            img = img.convert('RGB')
                            img.save(webp_file_path, 'webp', quality=20)

                            # Remove the original jpg file
                            os.remove(jpg_file_path)

                            return webp_file_path

            # If no results were returned or none of the images were large enough, continue to the next API key
            print("No suitable images found. Switching to the next API key...")
            continue

        except Exception as e:
            # If there is an API error (quota reached or other error), switch to the next API key and continue to the next iteration
            print(f"Exception: {e}")
            print("Switching to the next API key...")
            continue

    # If all API keys have reached the quota or there was an issue with all keys, return the default image
    print("All API keys have reached the quota or there was an issue with all keys.")
    return '/default.webp'  # Return default image if no images are found

# ... (previous code)

def generate_blog_post(tweet_data, word_limit, url):
    model = "gpt-3.5-turbo"
    content = tweet_data['text']
    author = tweet_data['author']['name']
    date = tweet_data['date']

    prompt = f'''
    Dear AI, I came across a tweet by {author} on {date} that goes like this: "{content}". It really caught my attention, and I think it would make an excellent topic for a short blog post. Could you help me with this? Please craft a compelling piece on it. Oh, and if the tweet has any kind of structured data or statistics, make sure to present it in a straightforward table for easy comprehension. Do remember to frame an interesting title, and if it's possible, incorporate numbers for impact. If the tweet concerns a person or place, be sure to mention their name in the title. Thanks!
    '''


    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a news blogger."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=word_limit,
        temperature=random.uniform(0.3, 0.7)
    )

    blog_post = response.choices[0].message['content']


    # Remove lines starting with "Date:" or "Body:"
    blog_post = "\n".join(line for line in blog_post.split('\n') if not line.strip().lower().startswith(('date:', 'body:')))

    blog_post = "\n".join(line for line in blog_post.split('\n') if "Introduction:" not in line and "Conclusion:" not in line)

    title = ""
    blog_post_html = ''
    intro_text = ""
    for i, line in enumerate(blog_post.splitlines()):
        line = line.strip()
        if line.lower().startswith('title:'):
            title = line[6:].strip()
            title = title.strip('"')
            title = title.replace('/', ' ')  # Add this line to replace slashes with spaces

    for i, line in enumerate(blog_post.splitlines()):
        line = line.strip()

    for i, line in enumerate(blog_post.splitlines()):
        line = line.strip()

        if len(line.split()) <= 20 and line.endswith(':'):
            blog_post_html += f'<h3>{line}</h3>\n'
        elif len(line.split()) <= 20 and not line.endswith(':'):
            blog_post_html += f'<div class="font-bold">{line}</div>\n'
        else:
            if not intro_text:  # If this is the first "long" paragraph, save it as intro_text
                intro_text = line
            else:
                blog_post_html += f'<p>{line}</p>\n'


    tweet_blockquote = f'<blockquote class="twitter-tweet"><a href="{url}"></a></blockquote>\n'
    tweet_blockquote += '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n'
    blog_post_html += tweet_blockquote

    # Get the image using the blog title as the keyword
    image_path = get_google_image(title)

    if image_path is not None:
        # Change image path from absolute to relative
        media_root = settings.MEDIA_ROOT
        if image_path.startswith(media_root):
            image_path = image_path[len(media_root):]
            if not image_path.startswith('/'):
                image_path = '/' + image_path
    else:
        image_path = ''  # Set an empty image path if no image is found

    return title, intro_text, blog_post_html, image_path


# ... (rest of the code)
from twitter.account import Account

ct0_cookie = '1623c9d82d1a7f1dae0f2799c6bc6de90937542a058b5fbe297baeb3e3af0297f7371d3faeaa8c30d6f3983f2e148aca463c9aa43e662c808c6518660638e095943eb534673889725778b1901e2c97ea'
auth_token_cookie = '051714fb57f27e9e747e1eef8817cfb10edb637b'



# Initialize Twitter account
account = Account(cookies={'ct0': ct0_cookie, 'auth_token': auth_token_cookie})
try:
    bookmarks = account.bookmarks()
    print("Successfully connected to the Twitter account.")
except Exception as e:
    print(f"Error connecting to the Twitter account: {e}")

# Fetch and print bookmarks
bookmarks = account.bookmarks()


for bookmark in bookmarks:
    data = bookmark.get('data', {})
    timeline = data.get('bookmark_timeline_v2', {}).get('timeline', {})
    instructions = timeline.get('instructions', [])
    
    for instruction in instructions:
        entries = instruction.get('entries', [])
        
        for entry in entries:
            entry_id = entry.get('entryId')
            if entry_id.startswith('tweet-'):
                tweet_id = entry_id[6:]
                url = f"https://twitter.com/foggy/status/{tweet_id}"
                try:
                    blog = GeneratedBlog.objects.get(bookmark_id=tweet_id)
                except GeneratedBlog.DoesNotExist:
                    tweet_data = entry['content']['itemContent']['tweet_results']['result']
                    tweet_text = ''  # Initialize tweet_text here

                    tweet_text = tweet_data.get('note_tweet', {}).get('note_tweet_results', {}).get('result', {}).get('text', '')
                    # If tweet_text is empty/not found, use the second pattern
                    if not tweet_text:
                        tweet_data = entry['content']['itemContent']['tweet_results']['result']['legacy']
                        tweet_text = tweet_data.get('full_text', '')

                    author_data = entry['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']
                    author_name = author_data.get('name', '')
                    print("Tweet Text:", tweet_text)
                    print("Author Name:", author_name)
                    
                    # Handle cases where "date" key is missing
                    date = tweet_data.get('created_at', '')

                    title, intro_text, blog_post_html, image_path = generate_blog_post(
                        {
                            'text': tweet_text,
                            'author': {
                                'name': author_name
                            },
                            'date': date
                        },
                        700,
                        url
                    )

                    if title.strip():
                        blog = GeneratedBlog(
                            bookmark_id=tweet_id,
                            author=author_name,
                            intro_text=intro_text,
                            blog_html_text=blog_post_html,
                            title=title,
                            image=image_path,
                            extra_context='To be generated'
                        )
                        blog.save()
                        print(f'Generated and saved blog post for tweet {tweet_id}')
                    else:
                        print(f'Could not generate title for blog post from tweet {tweet_id}. Blog post was not saved.')
