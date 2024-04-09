import os
import django
from django.utils import timezone
from datetime import timedelta
import openai
import os
import sys
sys.path.append('/home/rohit/news/website')
from fuzzywuzzy import fuzz
from collections import Counter

import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from pages.models import NewsChannel, Video, TrendingTopic, LiveNewsBulletin, Topic

openai.api_key = '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'  # replace with your OpenAI API key

print("Started processing...")

for topic in Topic.objects.all():
    print(f"Processing topic: {topic.name}")
    last_bulletin = LiveNewsBulletin.objects.filter(topic=topic).last()

    if last_bulletin:
        videos = Video.objects.filter(topic=topic.name, published_date__gt=last_bulletin.first_video_timestamp).order_by('published_date')
    else:
        videos = Video.objects.filter(topic=topic.name).order_by('published_date')

    if videos.count() >= 50:
        print(f"Topic {topic.name} has {videos.count()} videos since last bulletin. Processing...")
        video_batch = videos[:50]
        titles = ' '.join([video.title for video in video_batch]) 

        retry = 0
        while retry < 5:
            try:
                print("Attempting to generate summary...")
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": 'serious direct to point news writer, which doesnt write like a robot and dont make story yourself and plagrism free'},
                        {"role": "user", "content": f"I have news titles: {titles}. Can you summarize these in a single, short paragraph that forms a coherent narrative? Don't just list the titles or include things like 'In today's news'. For example: 'A school bus collided head-on with an SUV on the Delhi-Meerut Expressway on Tuesday morning. Six from a family died in the accident.'"},
                    ],
                    temperature=0.2, 
                    max_tokens=90, 
                )
                reply = completion.choices[0].message['content']
                if ',' in reply.split('. ')[0]:
                    reply = reply[reply.index(',')+2:]

                if len(reply) <= 5000:
                    reply = reply[:reply.rindex('.')+1]
                    reply = reply[0].upper() + reply[1:]

                    print(f"Generated summary: {reply}")

                    print("Saving news bulletin...")
                    LiveNewsBulletin.objects.create(
                        headline=reply,
                        topic=topic,
                        first_video_timestamp=video_batch[0].published_date,
                    )
                    print("News bulletin saved successfully!")
                    break

                else:
                    print(f"Generated reply was too long, retrying... Attempt {retry+1}")
                if retry == 4:
                    reply = reply[:5000]
                    print(f"Trimmed reply: {reply}")
                    break
                time.sleep(5)
            except Exception as e:
                print(f"Error on attempt {retry+1}: {e}")
                retry += 1
    else:
        print(f"Topic {topic.name} has less than 50 videos since last bulletin. Skipping...")

print("Processing complete!")
