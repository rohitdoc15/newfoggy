import sys
sys.path.append('/home/rohit/news/website')
from googletrans import Translator
import os
import django
from django.utils import timezone
from datetime import timedelta
from deep_translator import GoogleTranslator
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()
from collections import Counter as CollectionsCounter
from pages.models import NewsChannel, Video, TrendingTopic
import openai
import time

# Configure OpenAI API credentials
openai.api_key = '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'

# Get the current time
now = timezone.now()

# Get the time 4 hours ago
time_4_hours_ago = now - timedelta(hours=4)

# Fetch the top 5 distinct topics from the database
distinct_topics = TrendingTopic.objects.values_list('topic', flat=True).distinct()[:5]

# Translate function using translate package
def translate_to_english(text):
    translator = GoogleTranslator(source='auto', target='en')
    result = translator.translate(text)
    return result


# Iterate over each topic
for topic in distinct_topics:
    # Fetch the last 15 video titles of the given topic
    videos = Video.objects.filter(topic=topic).order_by('-published_date')[:15]
    titles = [video.title for video in videos]

    # Translate the titles using the translate package
    translated_titles = [translate_to_english(title) for title in titles]

    # Concatenate the translated titles into a single string
    titles_text = '\n'.join(translated_titles)
    completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": "news summariser"},
                        {"role": "user", "content": f"Generate a sarcastic(but not on) summary for the topic: {topic}\nTitles:\n{titles_text}. Generate very catchy tweet."},
                ],
                temperature = 0.2,
                
            )
    # Extract the model's reply
    synopsis = completion.choices[0].message['content']

    # Trim the synopsis to the nearest full stop if its length exceeds 150 words
    words = synopsis.split()
    if len(words) > 150:
        truncated_synopsis = ' '.join(words[:80])
        last_full_stop_index = truncated_synopsis.rfind('.')
        if last_full_stop_index != -1:
            synopsis = truncated_synopsis[:last_full_stop_index + 1]

    # Update the synopsis in the database
    trending_topic = TrendingTopic.objects.get(topic=topic)
    trending_topic.synopsis = synopsis
    trending_topic.save()

    print(f"Generated synopsis for topic '{topic}': {synopsis}")
