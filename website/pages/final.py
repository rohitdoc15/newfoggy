import sys
sys.path.append('/home/rohit/news/website')
from collections import Counter as CollectionsCounter
import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()
from pages.models import Video, TrendingTopic

# Get the current time
now = timezone.now()

# Stopword list
stopwords = ['India News','Latest English News (3', 'Breaking News','India','Aaj Tak', 'BJP','GD Vashist Astrology','The Quint','Sau Baat Ki Ek', 'Top Headlines', 'Viral Videos', 'Gravitas', 'National politics', 'Crime News', 'Hindi News', 'Weather Updates', 'Bihar News', 'R Bharat', 'World News', 'WION Shorts', 'News Events' , 'Delhi fire']

# Get the time 4 hours ago
time_4_hours_ago = now - timedelta(hours=12)

# Fetch all video topics from your database that were published in the last 4 hours
videos = Video.objects.filter(published_date__range=(time_4_hours_ago, now))

# Get topics from videos
topics = [video.topic for video in videos]

# Calculate the frequency of each topic
topic_counter = CollectionsCounter(topics)

# Filter out blank and dash ("-") topics and stop words
for topic in list(topic_counter):
    if topic == "" or topic == "-" or topic in stopwords:
        del topic_counter[topic]

# Get the 20 most common topics
most_common_topics = topic_counter.most_common(20)
print(f"Most common topics: {most_common_topics}")

# Update the TrendingTopic model
existing_topics = TrendingTopic.objects.all()
existing_topics.delete()  # Delete existing topics

for i, (topic, _) in enumerate(most_common_topics):
    trending_topic = TrendingTopic.objects.create(topic=topic, rank=i + 1)
    trending_topic.save()

distinct_topics = [topic for topic, _ in most_common_topics]

# Filter out stop words from top 5 distinct topics
top_5_distinct_topics = [topic for topic in distinct_topics if topic not in stopwords][:5]

print(f"Top 5 distinct topics: {top_5_distinct_topics}")
