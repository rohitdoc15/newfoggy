from django.shortcuts import render
from django.http import HttpResponse , JsonResponse ,FileResponse
# from . import templates
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
import html
from fuzzywuzzy import fuzz
from datetime import date
import requests
from operator import itemgetter

from .models import NewsChannel, TrendingTopic,Video
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from django.utils.text import slugify

from django.db.models import Count

from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from django.db.models.functions import TruncDate

from django.db.models import Count
from django.db.models.functions import TruncDate

from datetime import timedelta

def home(request):
    now = timezone.now()

    # Get the time 30 days ago
    time_30_days_ago = now - timedelta(days=30)

    # Get the time 8 hours ago
    time_8_hours_ago = now - timedelta(hours=4)
    time_16_hours_ago = now - timedelta(hours=12)

    news_channels = NewsChannel.objects.all()

    # Fetch all topics in a list
    all_trending_topics = list(TrendingTopic.objects.all())

    # Get the video count for each topic and store it in a dictionary
    topic_info = []
    for topic in all_trending_topics:
        # Only count videos that were published in the last 8 hours
        video_count = Video.objects.filter(topic=topic.topic, published_date__range=(time_8_hours_ago, now)).count()
        topic_info.append({
            'topic': topic,
            'count': video_count,
        })

    # Sort topics based on the video count in descending order
    sorted_topic_info = sorted(topic_info, key=lambda x: x['count'], reverse=True)

    for topic_info in sorted_topic_info:
        topic = topic_info['topic']
        count = topic_info['count']
        previous_8_hours_count = Video.objects.filter(topic=topic.topic, published_date__range=(time_16_hours_ago, time_8_hours_ago)).count()

        if previous_8_hours_count != 0:
            change_percentage = (count - previous_8_hours_count) / previous_8_hours_count * 100
        else:
            change_percentage = 0  # Set a default value or handle it appropriately
        print(count, previous_8_hours_count, change_percentage)
        # Determine the trend indicator based on the change percentage for each topic
        if change_percentage > 30:
            trend_indicator = 'upwards'
        elif change_percentage < -30:
            trend_indicator = 'downwards'
        else:
            trend_indicator = 'normal'
        
        topic_info['trend_indicator'] = trend_indicator
        print(topic_info)

    # Pick the top 5 topics
    top_5_topics = sorted_topic_info[:10]

    # Rest of your code...


    # Calculate top 5 topics from Video model based on video frequency over the last month
    top_5_video_topics_last_month = Video.objects.filter(published_date__range=(time_30_days_ago, now)).values('topic').annotate(count=Count('id')).order_by('-count')[:5]


    # Calculate the latest video timestamp
    latest_video_timestamp = Video.objects.latest('published_date').published_date

    context = {
        'channels': news_channels,
        'topic1': top_5_topics[0],
        'topic2': top_5_topics[1],
        'topic3': top_5_topics[2],
        'topic4': top_5_topics[3],
        'topic5': top_5_topics[4],
        'topic6': top_5_topics[5],
        'topic7': top_5_topics[6],
        'topic8': top_5_topics[7],
        'topic9': top_5_topics[8],
        'topic10': top_5_topics[9],
        'latest_video_timestamp': latest_video_timestamp,
    }




    return render(request, 'pages/home.html', context)

import json
from django.http import JsonResponse
from pages.models import sarso , petroluem,milk


def video_trend_chart(request, duration):
    now = timezone.now()

    if duration == "weekly":
        time_range = 7
        time_ago = now - timedelta(days=time_range)
        title_text = "Video Trend Over the Past 7 Days"
        xaxis_categories = [str(time_ago.date() + timedelta(days=i)) for i in range(time_range + 1)]
    else:
        time_range = 30
        time_ago = now - timedelta(days=time_range)
        title_text = "Video Trend Over the Past 30 Days"
        xaxis_categories = [str(time_ago.date() + timedelta(days=i)) for i in range(time_range + 1)]

    top_topics = Video.objects.filter(published_date__gte=time_ago) \
        .exclude(topic='') \
        .values('topic') \
        .annotate(video_count=Count('id')) \
        .order_by('-video_count')[:5]

    data = {
        "series": [],
        "labels": xaxis_categories,
        "chart": {
            "height": 350,
            "type": "line"
        },
        "title": {
            "text": title_text
        },
        "xaxis": {
            "categories": xaxis_categories
        },
    }

    for topic in top_topics:
        video_count_per_day = []
        for i in range(time_range + 1):
            date = time_ago + timedelta(days=i)
            video_count = Video.objects.filter(topic=topic['topic'], published_date__date=date).count()
            video_count_per_day.append(video_count)

        data["series"].append({
            "name": topic['topic'],
            "data": video_count_per_day
        })

    print(data)    

    return JsonResponse(data)

def inflation_chart_view(request):
    milk_data = milk.objects.values('date', 'price')
    sarso_data = sarso.objects.values('date', 'price')
    petroluem_data = petroluem.objects.values('date', 'price')
    
    milk_chart_data = [{'x': item['date'].strftime('%Y-%m-%d'), 'y': item['price']} for item in milk_data]
    sarso_chart_data = [{'x': item['date'].strftime('%Y-%m-%d'), 'y': item['price']} for item in sarso_data]
    petroluem_chart_data = [{'x': item['date'].strftime('%Y-%m-%d'), 'y': item['price']} for item in petroluem_data]
    
    chart_data = [
        {'name': 'Milk', 'data': milk_chart_data},
        {'name': 'Mustard Oil', 'data': sarso_chart_data},
        {'name': 'Petroluem', 'data': petroluem_chart_data}
    ]
    
    print(chart_data)
    return JsonResponse({'chart_data': chart_data})





from django.db import models



from django.http import JsonResponse

from django.db.models import Q



from django.http import JsonResponse

from django.urls import reverse
from django.http import JsonResponse

# def check_channel(request):
#     query = request.POST.get('search', '').strip()

#     if not query:
#         return JsonResponse({'results': []})

#     channel_results = NewsChannel.objects.filter(name__icontains=query)
#     topic_results = Video.objects.filter(topic__icontains=query).values('topic').annotate(video_count=models.Count('id')).filter(video_count__gt=50)

#     results_list = []
#     counter = 0  # Counter to track the number of results

from django.db.models import Count

def check_channel(request):
    query = request.POST.get('search', '').strip()

    if not query:
        return JsonResponse({'results': []})

    channel_results = NewsChannel.objects.filter(name__icontains=query)
    topic_results = Video.objects.filter(topic__icontains=query).values('topic').annotate(video_count=Count('id')).filter(video_count__gt=50)

    results_list = []
    counter = 0  # Counter to track the number of results

    for channel in channel_results:
        if counter >= 5:  # Break out of the loop once the limit is reached
            break

        result_dict = {
            'name': channel.name,
            'slug': channel.slug,
            'logo': channel.logo.url if channel.logo else None,  # Add the logo URL to the result dictionary
            'topics': [],
        }
        results_list.append(result_dict)
        counter += 1  # Increment the counter

    for topic in topic_results:
        if counter >= 5:  # Break out of the loop once the limit is reached
            break

        topic_data = {
            'topic': topic['topic'],
            'video_count': topic['video_count'],
        }
        results_list.append({'name': '', 'slug': '', 'logo': None, 'topics': [topic_data]})

        counter += 1  # Increment the counter
    print(results_list)    

    return JsonResponse({'results': results_list})



from django.shortcuts import render


from django.shortcuts import render
from .models import Video

from django.db.models import Min

from django.core.paginator import Paginator








from django.core.serializers.json import DjangoJSONEncoder
import json

from django.utils import formats

import operator
from datetime import datetime, timedelta
from django.utils import formats

from datetime import datetime, timedelta
from django.utils import formats
from django.db.models import Count,Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import Http404

def channel_name(request, slug):

    try:
        news_channel = NewsChannel.objects.get(slug=slug)
        channel_slugs = list(NewsChannel.objects.values_list('slug', flat=True))

        # Get the index of the current channel slug
        current_index = channel_slugs.index(slug)

        # Determine the index of the next channel slug
        next_index = (current_index + 1) % len(channel_slugs)

        # Retrieve the next channel slug
        next_slug = channel_slugs[next_index]

        # Retrieve the next channel based on the next slug
        next_channel = NewsChannel.objects.get(slug=next_slug)

        # Get the videos related to this channel
        videos = Video.objects.filter(channel=news_channel)

        # Filter videos from the past day and exclude blank or empty titles
        one_day_ago = datetime.now() - timedelta(days=1)
        day_videos = videos.filter(published_date__gte=one_day_ago).exclude(title__isnull=True).exclude(title='')

        # Get the count of each topic
        topic_counts = list(day_videos.values('topic').annotate(topic_count=Count('topic')).order_by('-topic_count'))

        # Decode HTML entities in topics and exclude null or empty topics
        topic_counts = [tc for tc in topic_counts if tc['topic']]
        
        # Merge duplicate topics and get the top five topics
        top_five_topics = merge_duplicate_topics(topic_counts)

        # Filter videos from the past week and exclude blank or empty titles for Modi and Rahul Gandhi count
        one_week_ago = datetime.now() - timedelta(weeks=1)  # Change the timedelta to 1 week
        week_videos = videos.filter(published_date__gte=one_week_ago).exclude(title__isnull=True).exclude(title='')
        
        # Define the religious terms
        religious_terms = ["हिन्दू", "मुस्लिम",]  # Replace with your actual religious terms

        # Count daily occurrences of "Modi", "Rahul Gandhi", and religious terms in the past week and compute percentages
        historical_counts = {}
        today = date.today()
        for i in range(7):
            current_date = today - timedelta(days=6 - i)  # Reverse the range
            total_videos = week_videos.filter(published_date__date=current_date).count()
            count_modi = week_videos.filter(published_date__date=current_date, title__icontains='Modi').count()
            count_rahul = week_videos.filter(published_date__date=current_date, title__icontains='Rahul Gandhi').count()
            count_religious = week_videos.filter(published_date__date=current_date, title__iregex=r'|'.join(religious_terms)).count()  # Use iregex to match any religious term
            formatted_date = current_date.strftime("%d %B")  # Format the date
            religious_percentage = round((count_religious / total_videos) * 100) if total_videos else 0  # Calculate religious term percentage
            historical_counts[formatted_date] = {
                "Modi": round((count_modi / total_videos) * 100) if total_videos else 0,
                "Rahul Gandhi": round((count_rahul / total_videos) * 100) if total_videos else 0,
                "Religious": religious_percentage  # Add religious percentage to historical_counts
                
            }
        upload_frequency = [week_videos.filter(published_date__date=current_date).count() for current_date in [today - timedelta(days=i) for i in range(6, -1, -1)]]

        # Videos pagination
        videos_list = videos.order_by('-published_date')
        page = request.GET.get('page', 1)  # Get the page number from the query string
        paginator = Paginator(videos_list, 5)  # Show 5 videos per page

        try:
            paginated_videos = paginator.page(page)
        except PageNotAnInteger:
            paginated_videos = paginator.page(1)  # If page is not an integer, deliver first page.
        except EmptyPage:
            paginated_videos = paginator.page(paginator.num_pages)  # If page is out of range, deliver last page of results.

        context = {
            "channel": news_channel,
            "youtube_channel": news_channel.youtube_channel,
            "twitter_handle": news_channel.twitter_handle,
            "facebook_page": news_channel.facebook_page,
            "topic_counts": top_five_topics,
            "historical_counts": json.dumps(historical_counts, cls=DjangoJSONEncoder),
            "upload_frequency": upload_frequency,
            "videos": paginated_videos,
            "next_channel_slug": next_slug,
            "next_channel": next_channel,
        }
        print(upload_frequency)
        return render(request, 'pages/channelname.html', context)
    except NewsChannel.DoesNotExist:
        raise Http404("NewsChannel matching query does not exist.")



from bs4 import BeautifulSoup
import requests
from django.views import View
from django.http import JsonResponse

class LiveVideoTitleView(View):
    def get(self, request, *args, **kwargs):
        youtube_url = request.GET.get('youtube_url')
        if youtube_url:
            url = youtube_url + '/live'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            title_element = soup.find("title")
            print(title_element)

            if title_element:
                title = title_element.text.strip()
                if title.endswith(" - YouTube"):
                    title = title[:-10]  # Remove the last 10 characters
                if len(title) > 20:
                    return JsonResponse({'title': title})
            
            title = "No live broadcast available"
            return JsonResponse({'title': title})
            
        
        return JsonResponse({'error': 'Invalid YouTube URL'}, status=400)




def merge_duplicate_topics(topic_counts):
    merged_topics = []

    for topic1 in topic_counts:
        topic_count = topic1['topic_count']
        merged_topic = topic1['topic']
        duplicate_found = False

        for topic2 in merged_topics:
            ratio = fuzz.token_sort_ratio(topic1['topic'], topic2['topic'])
            if ratio > 50:
                merged_topic = shorter_string(merged_topic, topic2['topic'])
                topic_count += topic2['topic_count']
                duplicate_found = True

        if not duplicate_found:
            merged_topics.append({'topic': merged_topic, 'topic_count': topic_count})

    merged_topics.sort(key=lambda x: x['topic_count'], reverse=True)

    return merged_topics[:5]


def shorter_string(str1, str2):
    return str1 if len(str1) <= len(str2) else str2




def cloud(request):
    result = request.POST.get('name')
    print(result)
    context = {'results': result}
    return render(request, 'pages/cloud.html',context)

from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from .models import TrendingTopic, Video

from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from .models import TrendingTopic, Video

from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Video

def apex(request):
    # Date 30 days ago from now
    one_month_ago = timezone.now() - timedelta(days=30)

    # Get top 5 topics based on video frequency over the past 30 days
    top_topics = Video.objects.filter(published_date__gte=one_month_ago)\
        .values('topic')\
        .annotate(video_count=Count('id'))\
        .order_by('-video_count')[:5]

    # Initialize data dictionary for ApexChart
    data = {
        "series": [],
        "labels": [str(one_month_ago.date() + timedelta(days=i)) for i in range(30)],
        "chart": {
            "height": 350,
            "type": "line"
        },
        "title": {
            "text": 'Video Trend Over the Past 30 Days'
        },
        "xaxis": {
            "categories": [str(one_month_ago.date() + timedelta(days=i)) for i in range(30)]
        },
    }

    # For each of the top 5 topics, get the daily video count for the past 30 days
    for topic in top_topics:
        video_count_per_day = []
        for i in range(30):
            date = one_month_ago + timedelta(days=i)
            video_count = Video.objects.filter(topic=topic['topic'], published_date__date=date).count()
            video_count_per_day.append(video_count)

        # Append this topic's data to the series list
        data["series"].append({
            "name": topic['topic'],
            "data": video_count_per_day
        })
        print(data)

    return render(request, 'pages/apex.html', {'data': data})


def story(request, channel_name):
    news_channel = get_object_or_404(NewsChannel, name=channel_name)
    all_channels = NewsChannel.objects.all()
    context = {'channel': news_channel, 'channels': all_channels}
    return render(request, 'pages/story.html', context)




from django.shortcuts import render
import json

from django.db.models import Count
from pages.models import Video

def heatmap(request):
    # Get a list of topics that have more than 50 videos associated with them
    # Original queryset
    topics = Video.objects.values('topic').annotate(video_count=Count('topic')).filter(video_count__gt=50)

    # Transformation
    heatmap_data = []
    for topic in topics:
        heatmap_dict = {}
        # For example, we map the first character of the topic to a day in the month
        heatmap_dict['day'] = ord(topic['topic'][0]) % 31 + 1
        # And we map the video count to an hour in the day
        heatmap_dict['hour'] = topic['video_count'] % 24
        # And we use the video count as the count (you could use a different property here if you prefer)
        heatmap_dict['count'] = topic['video_count']
        heatmap_data.append(heatmap_dict)

    return render(request, 'pages/heatmap.html', {'topics': heatmap_data})



import requests
from django.shortcuts import render

def fact_check(request, search_term=None, return_results=False):
    if not search_term:
        search_term = request.GET.get('search_term', '')  # Get the search term from the request

    if search_term:
        # Perform the fact check API request
        api_key = 'AIzaSyB9BgMqW9AXGQD0ZfHWgFrtq6tTz9WEUVo'  # Replace with your actual API key
        url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?key={api_key}"
        params = {
            'query': search_term,
            'pageSize': 10,
            'languageCode': 'en',
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            fact_checks = data.get('claims', [])

            if return_results:
                # If the return_results argument is True, return the fact checks as a list
                return fact_checks

            # Otherwise, render the template with the fact checks, search term, and error message (if any)
            context = {
                'fact_checks': fact_checks,
                'search_term': search_term,
                'error_message': None,
            }
            return render(request, 'pages/factcheck.html', context)
        except requests.exceptions.RequestException as e:
            error_message = f"Error occurred: {str(e)}"
            context = {
                'fact_checks': [],
                'search_term': search_term,
                'error_message': error_message,
            }
            return render(request, 'pages/factcheck.html', context)

    # Render the template with the search form
    return render(request, 'pages/factcheck.html')


from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def fact_check_view(request):
    search_term = request.GET.get('search_term', '')
    fact_checks = fact_check(request, search_term, return_results=True)
    print(fact_checks)
    return JsonResponse({'fact_checks': fact_checks[:5]})


from bs4 import BeautifulSoup

@require_GET
def fact_check_proxy(request):
    url = request.GET.get('url', '')
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    og_image = soup.find('meta', {'property': 'og:image'})

    return JsonResponse({'image_url': og_image.get('content') if og_image else None})



from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

from django.shortcuts import render

from datetime import datetime, timedelta

from django.shortcuts import render
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import NewsChannel, Video, TrendingTopic
import json

@csrf_exempt
def topic_page(request):
    if request.method == 'POST':
        topic = request.POST.get('topic', '')
        top_channels = NewsChannel.objects.annotate(video_count=Count('videos', filter=Q(videos__topic=topic))).order_by('-video_count')[:5]

        # Retrieve the synopsis for the topic
        try:
            trending_topic = TrendingTopic.objects.get(topic=topic)
            synopsis = trending_topic.synopsis
        except TrendingTopic.DoesNotExist:
            synopsis = ""

        # Retrieve the last video for the topic
        last_video = Video.objects.filter(topic=topic).order_by('-published_date').first()
        last_video_thumbnail_url = last_video.thumbnail_url if last_video else None

        # Count the videos for the topic
        video_count = Video.objects.filter(topic=topic).count()

        # Get the first video for the topic
        first_video = Video.objects.filter(topic=topic).order_by('published_date').first()
        first_appeared_date = first_video.published_date if first_video else None

        # Count the videos for the last seven days
        today = datetime.now().date()
        seven_days_ago = today - timedelta(days=6)
        daily_counts = []
        day_labels = []
        for i in range(7):
            current_date = seven_days_ago + timedelta(days=i)
            count = Video.objects.filter(topic=topic, published_date__date=current_date).count()
            daily_counts.append(count)
            day_labels.append(current_date.strftime("%b %d"))  # Add formatted day labels

        # Get the latest 5 videos
        latest_videos = Video.objects.filter(topic=topic).order_by('-published_date')[:5]

        context = {
            'title': topic,
            'top_channels': top_channels,
            'synopsis': synopsis,
            'last_video_thumbnail_url': last_video_thumbnail_url,
            'topic_count': video_count,
            'first_appeared_date': first_appeared_date,
            'daily_counts': daily_counts,
            'daily_counts_json': json.dumps(daily_counts),  # Convert daily_counts to JSON
            'day_labels': day_labels,  # Pass day labels to template
            'latest_videos': latest_videos,
        }

        return render(request, 'pages/topic_page.html', context)
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=400)
from functools import reduce


from django.shortcuts import render
from django.db.models import Q

def topic_details(request, topic=None):
    if request.method == 'POST':
        if topic is None:
            topic = request.POST.get('topic', '')
    elif request.method == 'GET':
        if topic is None:
            topic = request.GET.get('topic', '')
    else:
        return JsonResponse({"error": "Only GET and POST methods are allowed."}, status=400)

    top_channels = NewsChannel.objects.annotate(video_count=Count('videos', filter=Q(videos__topic=topic))).order_by('-video_count')[:5]

    # Retrieve the synopsis for the topic
    try:
        trending_topic = TrendingTopic.objects.get(topic=topic)
        synopsis = trending_topic.synopsis
    except TrendingTopic.DoesNotExist:
        synopsis = ""

    # Retrieve the last video for the topic
    last_video = Video.objects.filter(topic=topic).order_by('-published_date').first()
    last_video_thumbnail_url = last_video.thumbnail_url if last_video else None

    # Count the videos for the topic
    video_count = Video.objects.filter(topic=topic).count()

    # Get the first video for the topic
    first_video = Video.objects.filter(topic=topic).order_by('published_date').first()
    first_appeared_date = first_video.published_date if first_video else None

    # Get all-time historical daily counts
    all_time_counts = Video.objects.filter(topic=topic).values('published_date__date').annotate(count=Count('id')).order_by('published_date__date')
    daily_counts = [entry['count'] for entry in all_time_counts]
    day_labels = [entry['published_date__date'].strftime("%b %d") for entry in all_time_counts]

    # Get the latest 5 videos
    latest_videos = Video.objects.filter(topic=topic).order_by('-published_date')[:5]

    # Split the topic into individual words
    topic_words = topic.split()

    # Get related topics based on matching words and more than 50 videos
    related_topics = Video.objects.filter(
        reduce(lambda x, y: x | y, [Q(topic__icontains=word) for word in topic_words])
    ).exclude(topic=topic).values('topic').annotate(video_count=Count('id')).filter(video_count__gt=50).order_by('-video_count')[:3]

    context = {
        'title': topic,
        'top_channels': top_channels,
        'synopsis': synopsis,
        'last_video_thumbnail_url': last_video_thumbnail_url,
        'topic_count': video_count,
        'first_appeared_date': first_appeared_date,
        'daily_counts': daily_counts,
        'daily_counts_json': json.dumps(daily_counts),  # Convert daily_counts to JSON
        'day_labels': day_labels,  # Pass day labels to template
        'latest_videos': latest_videos,
        'related_topics': related_topics,
    }
    print(related_topics   )

    return render(request, 'pages/topic_details.html', context)



from django.shortcuts import render
from django.db.models import Count, Avg

from django.db.models import Count, F, FloatField, ExpressionWrapper
from datetime import datetime, timedelta

from django.db.models import Count, F, FloatField, ExpressionWrapper
from datetime import datetime, timedelta

from django.db.models import Count, F, FloatField, ExpressionWrapper
from datetime import datetime, timedelta

def channel_list(request):
    seven_days_ago = datetime.now() - timedelta(days=7)
    channels = NewsChannel.objects.annotate(video_count=Count('videos')).order_by('youtube_rank')

    for channel in channels:
        videos_per_day = Video.objects.filter(
            channel=channel,
            published_date__gte=seven_days_ago
        ).count() / 7
        channel.avg_videos_per_day = round(videos_per_day, )

        channel.fake_news_rating = channel.fake_news_index
        channel.credibility = channel.credibility_index

    context = {
        'channels': channels
    }

    return render(request, 'pages/channel_list.html', context)


from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from .models import NewsChannel, Video

def channel_list(request):
    seven_days_ago = datetime.now() - timedelta(days=7)
    channels = NewsChannel.objects.annotate(video_count=Count('videos')).order_by('youtube_rank')

    for channel in channels:
        videos_per_day = Video.objects.filter(
            channel=channel,
            published_date__gte=seven_days_ago
        ).count() / 7
        channel.avg_videos_per_day = round(videos_per_day)

        channel.fake_news_rating = channel.fake_news_index
        channel.credibility = channel.credibility_index

    context = {
        'channels': channels
    }

    return render(request, 'pages/channel_list.html', context)


def keyword_video_count(request):
    bjp_keywords = [
        'modi', 'bjp', 'narendra modi',  # English keywords
        'मोदी', 'भाजपा', 'नरेंद्र मोदी'  # Hindi keywords
    ]

    aap_keywords = [
        'kejriwal', 'aam admi party', 'arvind kejriwal', 'manish sisodia'  # English keywords
        'केजरीवाल', 'आम आदमी पार्टी', 'अरविंद केजरीवाल'  # Hindi keywords
    ]

    congress_keywords = [
        'rahul gandhi', 'congress', 'sonia gandhi',  # English keywords
        'राहुल गांधी', 'कांग्रेस', 'सोनिया गांधी'  # Hindi keywords
    ]

    shivsena_keywords = [
        'uddhav thackeray', 'shiv sena', 'aditya thackeray',  # English keywords
        'उद्धव ठाकरे', 'शिवसेना', 'आदित्य ठाकरे'  # Hindi keywords
    ]

    tmc_keywords = [
        'mamata banerjee', 'trinamool congress', 'abhishek banerjee', 'TMC', # English keywords
        'ममता बनर्जी', 'तृणमूल कांग्रेस', 'अभिषेक बनर्जी'  # Hindi keywords
    ]

    sp_keywords = [
        'mulayam singh yadav', 'samajwadi party', 'akilesh yadav',  # English keywords
        'मुलायम सिंह यादव', 'समाजवादी पार्टी', 'अखिलेश यादव'  # Hindi keywords
    ]

    # Combine all the keywords into a single list
    all_keywords = bjp_keywords + aap_keywords + congress_keywords + shivsena_keywords + tmc_keywords + sp_keywords

    # Get the last 2 days' news videos
    two_days_ago = timezone.now() - timezone.timedelta(days=2)
    news_videos = Video.objects.filter(published_date__gte=two_days_ago)

    # Get all news channels
    news_channels = NewsChannel.objects.all()
    total_videos = 0

    # Initialize the dictionary to store the party scores
    party_scores = {
        'BJP': 0,
        'AAP': 0,
        'Congress': 0,
        'Shiv Sena': 0,
        'Trinamool Congress': 0,
        'Samajwadi Party': 0
    }

    # Iterate through the news titles and calculate the scores for each party
    for video in news_videos:
        title = video.title.lower()

        # Initialize the flag to check if any party keyword is found
        party_found = False

        # Check for BJP keywords
        for keyword in bjp_keywords:
            if keyword in title:
                party_scores['BJP'] += 1
                party_found = True
                break

        # Check for AAP keywords
        for keyword in aap_keywords:
            if keyword in title:
                party_scores['AAP'] += 1
                party_found = True
                break

        # Check for Congress keywords
        for keyword in congress_keywords:
            if keyword in title:
                party_scores['Congress'] += 1
                party_found = True
                break

        # Check for Shiv Sena keywords
        for keyword in shivsena_keywords:
            if keyword in title:
                party_scores['Shiv Sena'] += 1
                party_found = True
                break

        # Check for Trinamool Congress keywords
        for keyword in tmc_keywords:
            if keyword in title:
                party_scores['Trinamool Congress'] += 1
                party_found = True
                break

        # Check for Samajwadi Party keywords
        for keyword in sp_keywords:
            if keyword in title:
                party_scores['Samajwadi Party'] += 1
                party_found = True
                break


        if party_found:

            for party, keywords in zip(party_scores.keys(), [bjp_keywords, aap_keywords, congress_keywords,
                                                             shivsena_keywords, tmc_keywords, sp_keywords]):
                if any(keyword in title for keyword in keywords):
                    print( end=" ")
            
        if party_found:
            total_videos += 1
    

 
    print(f"Total videos: {total_videos}")       

    # Return the JSON response with the party scores
    return JsonResponse(party_scores)



from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from datetime import timedelta
from .models import TopPopularPersons
from django.views.generic import View
from django.http import JsonResponse
from .models import TopPopularPersons

class PopularPersonChartView(View):
    def get(self, request):
        data = {
            'chart': {'type': 'line'},
            'series': [{'name': 'Popular Person', 'data': []}],
            'xaxis': {'categories': []}
        }

        # Retrieve the last 20 days' data
        top_persons = TopPopularPersons.objects.order_by('-date')[:20]

        # Populate the chart data
        for person in top_persons:
            person_data = f"{person.person1_name} ({person.person1_video_count})"
            data['series'][0]['data'].append(person_data)
            data['xaxis']['categories'].append(str(person.date))

       
        return JsonResponse(data)
def contact(request):
    result = request.POST.get('name')
    print(result)
    context = {'results': result}
    return render(request, 'pages/contact.html',context)


def privacy_view(request):
    return render(request, 'pages/privacy_policy.html')

def about(request):
    result = request.POST.get('name')
    print(result)
    context = {'results': result}
    return render(request, 'pages/about.html',context)


from django.db.models import Count
from django.db.models.functions import Lower
from django.views import generic
from .models import Video


class TopicGlossaryView(generic.ListView):
    model = Video
    template_name = 'pages/topic_glossary.html'
    context_object_name = 'topics'

    def get_queryset(self):
        topics = Video.objects.values('topic').annotate(video_count=Count('topic')).order_by(Lower('topic'))
        topic_dict = {}
        for topic in topics:
            if topic['topic']:
                first_letter = topic['topic'][0].upper()
                if first_letter not in topic_dict:
                    topic_dict[first_letter] = [(topic['topic'], topic['video_count'])]
                else:
                    topic_dict[first_letter].append((topic['topic'], topic['video_count']))
        return topic_dict


from django.http import JsonResponse
from django.core import serializers
from django.views import View
from .models import LiveNewsBulletin, Topic
from django.core.exceptions import ObjectDoesNotExist

from django.core import serializers
from json import loads

# ...

class LiveNewsBulletinDataView(View):
    def get(self, request, *args, **kwargs):
        topic_name = request.GET.get('topic', None)
        limit = int(request.GET.get('limit', 4))
        offset = int(request.GET.get('offset', 0))
        
        if topic_name is None:
            return JsonResponse({"error": "Missing topic parameter"}, status=400)

        try:
            topic = Topic.objects.get(name=topic_name)
        except ObjectDoesNotExist:
            return JsonResponse({"error": f"No topic with the name {topic_name} found."}, status=404)

        bulletins = LiveNewsBulletin.objects.filter(topic=topic).order_by('-timestamp')  # Sort by descending timestamp
        total_bulletins = bulletins.count()
        
        bulletins = bulletins[offset:offset+limit]
        bulletins_data = serializers.serialize('json', bulletins)

        # Deserialize the serialized data into Python data structures
        bulletins_data = loads(bulletins_data)

        # Convert the list of Django objects into a list of dictionaries
        bulletins_list = [bulletin['fields'] for bulletin in bulletins_data]
        
        response_data = {
            'total_bulletins': total_bulletins,
            'bulletins': bulletins_list,
        }
        return JsonResponse(response_data, safe=False)


from django.http import JsonResponse
from django.views import View
import aiohttp
import asyncio
from lxml import html
import time

class ImageSearchView(View):
    async def get_image_url(self, session, search_term):
        url = "https://www.bing.com/images/search?q={}".format(search_term.replace(' ', '%20'))
        response = await session.get(url)
        tree = html.fromstring(await response.text())
        image = tree.xpath('//img[@class="mimg"]')[0]
        return search_term, image.attrib['src']

    async def get_first_image_url(self, search_terms):
        start_time = time.time()

        async with aiohttp.ClientSession() as session:
            tasks = [self.get_image_url(session, term) for term in search_terms]
            results = await asyncio.gather(*tasks)

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"The function took {elapsed_time} seconds to run.")
        return dict(results)

    def get(self, request, *args, **kwargs):
        # The search terms can be passed as a GET parameter, for example:
        # /image_search/?terms=virat%20kohli%20pic,dhoni%20pic,pm%20modi,amit%20shah,kapil%20dev
        search_terms = request.GET.get('terms', '').split(',')
        results = asyncio.run(self.get_first_image_url(search_terms))
        return JsonResponse(results)




from .models import TopPopularPersons

from collections import Counter

def analysis_view(request):
    # Get today's date
    today = timezone.now().date()

    # Calculate the date 100 days ago
    hundred_days_ago = today - timedelta(days=100)

    # Query the database for the top persons from the last 100 days
    top_persons = TopPopularPersons.objects.filter(date__gte=hundred_days_ago)

    # Extract the names of the top persons
    person_names = [person.person1_name for person in top_persons]

    # Count the frequency of each person and get the top 3
    most_common_persons = Counter(person_names).most_common(3)

    # Extract just the names of the top 3 persons
    top_3_person_names = [person[0] for person in most_common_persons]

    # Get the top 3 news channels with the most subscribers
    top_3_channels = NewsChannel.objects.all().order_by('-subscribers')[:3]

    # Get the top 5 trending topics
    top_5_topics = TrendingTopic.objects.all().order_by('rank')[:5]

    # Pass the person names, channel logos, and topics to the template
    context = {
        'person_names': top_3_person_names,
        'channels': top_3_channels,
        'topics': top_5_topics,
    }
    return render(request, 'pages/analysis.html', context)



def topic_analysis_view(request):
    # Your code here
    pass

def person_analysis_view(request):
    # Your code here
    return render(request, 'pages/person.html')


def channel_analysis_view(request):
    # Your code here
    pass








import re
import html

import string

import requests
from lxml import html

from requests_html import HTMLSession

class LiveSearchView(View):
    def get_images(self, phrases):
        session = HTMLSession()

        images = {}
        for phrase in phrases:
            url = "https://www.bing.com/images/search?q={}".format(phrase.replace(' ', '%20'))
            response = session.get(url)
            image = response.html.find('.mimg', first=True)
            if image:
                images[phrase] = image.attrs.get('src', "")

        return images

    def get(self, request):
        search_term = request.GET.get('term', '')
        videos = Video.objects.filter(Q(title__icontains=search_term))[:5]

        # Extract the titles of the videos and split them into words
        words = [word for title in videos.values_list('title', flat=True) for word in title.translate(str.maketrans('', '', string.punctuation)).split()]

        # Form bigrams from the words
        bigrams = [(words[i], words[i + 1]) for i in range(len(words) - 1)]

        # Check each bigram if the first word starts with the search term, and second word is in English
        matching_bigrams = [bigram for bigram in bigrams if bigram[0].lower().startswith(search_term.lower()) and re.match("^[A-Za-z]*$", bigram[1])]

        # Convert bigrams to strings and remove duplicates
        matching_phrases = list(set([' '.join(bigram) for bigram in matching_bigrams]))

        # Find the first full word that matches the search term
        full_word_match = next((word for word in words if word.lower().startswith(search_term.lower())), None)

        if full_word_match:
            # If a full word match was found, remove it from the list and insert it at the beginning
            if full_word_match in matching_phrases:
                matching_phrases.remove(full_word_match)
            matching_phrases.insert(0, full_word_match)

        # Only keep the first 3 results
        matching_phrases = matching_phrases[:3]

        # Fetch images for matching phrases
        images = self.get_images(matching_phrases)

        # Create response data where keys are names and values are image URLs
        data = {phrase: images.get(phrase, "") for phrase in matching_phrases}

        # Respond with the data as JSON
        return JsonResponse(data)



class PersonDetailView(View):
    def get(self, request, person_name):
        # Retrieve the person's details. Here's a mock example, replace with your actual logic.
        person_details = {
            'name': person_name,
            'age': 30,
            'bio': 'Some bio text...'
        }
        print(person_details)
        return render(request, 'pages/person_details.html', person_details)


import html

class VideoView(View):
    def get(self, request, *args, **kwargs):
        videos = Video.objects.all().order_by('published_date') 

        term = self.request.GET.get('term', None)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        channels = self.request.GET.get('channels', None)

        if term:
            videos = videos.filter(Q(title__icontains=term) | Q(transcript__icontains=term))

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            videos = videos.filter(published_date__range=[start_date, end_date])

        if channels:
            channels = channels.split(',')
            videos = videos.filter(channel__id__in=channels)  

        # Using annotate to rename the 'channel__name' field to 'channel_name'
        videos = videos.annotate(channel_name=F('channel__name'))

        # Get up to 500 videos at once
        videos = videos[:500]

        data = list(videos.values('channel_name', 'title', 'published_date'))

        for video in data:
            video['title'] = html.unescape(video['title']) 

        return JsonResponse(data, safe=False)

class ChannelView(View):
    def get(self, request, *args, **kwargs):
        channels = NewsChannel.objects.all().values('id', 'name')
        return JsonResponse(list(channels), safe=False)    
    






from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import GeneratedBlog

class Bloghome(ListView):
    model = GeneratedBlog
    template_name = 'pages/blog/index.html'
    paginate_by = 30  # Number of blog posts to display per page

    def get_queryset(self):
        return GeneratedBlog.objects.order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['random_blogs'] = GeneratedBlog.objects.order_by('?')[:4]
        return context


from django.http import JsonResponse
from django.core import serializers

from django.core.paginator import Paginator

def blog_post(request, blog_title):
    blog = get_object_or_404(GeneratedBlog, title=blog_title)

    latest_blogs = GeneratedBlog.objects.order_by('-pub_date')[:4]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        blog_json = serializers.serialize('json', [blog])
        return JsonResponse(blog_json, safe=False)

    return render(request, 'pages/blog/article.html', {'blog': blog, 'latest_blogs': latest_blogs})




from django.http import JsonResponse
from django.core import serializers
from django.urls import reverse

def load_more_blogs(request):
    last_blog_id = request.GET.get('last_blog_id', None)

    if last_blog_id is not None:
        # Get the last blog's pub_date
        last_blog_pub_date = GeneratedBlog.objects.get(bookmark_id=last_blog_id).pub_date

        # Fetch the next set of 4 blogs with pub_date older than the last_blog_pub_date
        blogs = GeneratedBlog.objects.filter(pub_date__lt=last_blog_pub_date).order_by('-pub_date')[:4]

        blogs_data = []
        for blog in blogs:
            blog_data = {
                "fields": {
                    "title": blog.title,
                    "image": blog.image.url,
                    "blog_html_text": blog.blog_html_text,
                    "author": blog.author,
                    "pub_date": blog.pub_date.strftime("%d %b %Y"),
                },
                "url": reverse('blog-detail', args=[blog.title]),
                "pk": blog.bookmark_id,
            }
            blogs_data.append(blog_data)
        return JsonResponse(blogs_data, safe=False)

    return JsonResponse({}, status=400)  # Return an error response if no last_blog_id was provided

from django.contrib.sitemaps import Sitemap


from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import GeneratedBlog

from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import GeneratedBlog

class RequestFeed(Feed):
    request = None

    def __call__(self, request, *args, **kwargs):
        self.request = request
        return super().__call__(request, *args, **kwargs)

class LatestPostsFeed(RequestFeed):
    title = "My Blog"
    link = "/rss/"
    description = "Latest Posts"

    def items(self):
        return GeneratedBlog.objects.order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        img_url = self.request.build_absolute_uri(item.image.url) if item.image else ''
        return f'<img src="{img_url}" alt="">{item.intro_text}'

    def item_link(self, item):
        return reverse('blog-detail', args=[item.title])
