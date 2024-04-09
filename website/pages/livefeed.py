import sys
import time
sys.path.append('/home/rohit/news/website')
from googletrans import Translator
translator = Translator()
import os
import django
from django.utils import timezone
from datetime import timedelta
import openai
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')  
django.setup()
from collections import Counter as CollectionsCounter
from pages.models import NewsChannel, Video, TrendingTopic, LiveNewsBulletin, Topic

openai.api_key = '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'  # replace with your OpenAI API key

print("Started processing...")

for topic in Topic.objects.all():
    print(f"Processing topic: {topic.name}")
    videos = Video.objects.filter(topic=topic.name).order_by('published_date')
    if videos.count() >= 50:  # Only process topics with 50 or more videos
        print(f"Topic {topic.name} has {videos.count()} videos. Processing...")
        for i in range(0, videos.count(), 50):
            print(f"Processing batch starting at index: {i}")
            video_batch = videos[i:i+50]
            titles = ' '.join([video.title for video in video_batch])  # Combine all titles into a single string
            
            retry = 0
            while retry < 5:  # Continue until we get a reply under 5000 characters
                try:
                    # Construct the conversation with the AI model
                    print("Attempting to generate summary...")
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": 'serious direct to point news writer, which doesnt write like a robot and dont make story yourself and plagrism free'},
                            {"role": "user", "content": f"I have news titles: {titles}. Can you summarize these in a single, short paragraph that forms a coherent narrative? Don't just list the titles or include things like 'In today's news'. For example: 'A school bus collided head-on with an SUV on the Delhi-Meerut Expressway on Tuesday morning. Six from a family died in the accident.'"},
                        ],
                        temperature=0.2, # Lower temperature for more deterministic output
                        max_tokens=90,  # limit the response length

                    )
                    # Extract the model's reply
                    reply = completion.choices[0].message['content']
                    
                    if ',' in reply.split('. ')[0]:
                        reply = reply[reply.index(',')+2:]

                    # Check if the reply is under 5000 characters
                    if len(reply) <= 5000:
                        reply = reply[:reply.rindex('.')+1]  # rindex() finds the last occurrence
                        # Capitalize the first letter of the reply
                        reply = reply[0].upper() + reply[1:]


                        print(f"Generated summary: {reply}")
                        
                        # Save the news bulletin
                        print("Saving news bulletin...")
                        LiveNewsBulletin.objects.create(
                            headline=reply,
                            topic=topic,
                            first_video_timestamp=video_batch[0].published_date,  # set first_video_timestamp here

                        )
                        print("News bulletin saved successfully!")
                        
                        break
                    else:
                        print(f"Generated reply was too long, retrying... Attempt {retry+1}")
                    if retry == 4:
                        reply = reply[:5000]  # Trim the reply to 5000 characters
                        print(f"Trimmed reply: {reply}")
                        break
                    time.sleep(5)  # Wait for 5 seconds before retrying
                except Exception as e:
                    print(f"Error on attempt {retry+1}: {e}")
                    retry += 1  # Increase the retry count only when an exception occurs

    else:
        print(f"Topic {topic.name} has less than 50 videos. Skipping...")
print("Processing complete!")
