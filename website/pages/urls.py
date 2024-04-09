from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from pages.views import inflation_chart_view
from django.contrib.sitemaps.views import sitemap

urlpatterns = [
    path('', views.home , name='home'),
   
    
]
from django.urls import path
from django.contrib.sitemaps import Sitemap
from .models import GeneratedBlog

from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps.views import sitemap


from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import reverse
from django.urls import path
from .models import GeneratedBlog
from . import views  # ensure your views are imported

class BlogSitemap(Sitemap):
    def items(self):
        return GeneratedBlog.objects.all()

    def location(self, obj):
        return reverse('blog-detail', args=[urllib.parse.quote(obj.title)])

sitemaps = {
    'blogs': BlogSitemap,
}



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

htmx_url_patterns = [
         path('check_channel/', views.check_channel , name='check_channel'),
         path('searchlist/', views.check_channel , name='searchlist'),
         path('channel/<str:slug>/',views.channel_name, name='channel_name'), 
         path('cloud/',views.cloud, name='cloud'),
         path('apex/',views.apex, name='apex'),
         path('story/<str:channel_name>/', views.story, name='story'),
         path('heatmap/', views.heatmap, name='heatmap'),
         path('fact-check/', views.fact_check, name='fact_check'),
         path('topic-page/', views.topic_page, name='topic_page'),
         path('fact-check-view/', views.fact_check_view, name='fact_check_view'),
         path('topic/<str:topic>/', views.topic_details, name='topic_details'),
         path('inflation-chart-data/', inflation_chart_view, name='inflation-chart-data'),
         path('channels/', views.channel_list, name='channel_list'),
         path('video-count/', views.keyword_video_count, name='video_count'),
         path('popular-person-chart/', views.PopularPersonChartView.as_view(), name='popular_person_chart'),
         path('api/live_video_title', views.LiveVideoTitleView.as_view(), name='live_video_title'),
         path('contact/', views.contact, name='contact'),
         path('privacy_policy/', views.privacy_view, name='privacy'),
         path('about/',views.about, name='about'),
         path('fact-check-proxy/', views.fact_check_proxy, name='fact_check_proxy'),
         path('video-trend-chart/<str:duration>/', views.video_trend_chart, name='video_trend_chart'),
         path('glossary/', views.TopicGlossaryView.as_view(), name='topic_glossary'),
         path('bulletins/', views.LiveNewsBulletinDataView.as_view(), name='live_bulletins_data'),
         path('image_search/', views.ImageSearchView.as_view(), name='image_search'),
        path('analysis/', views.analysis_view, name='analysis'),
        path('analysis/topic/', views.topic_analysis_view, name='topic_analysis'),
        path('analysis/person/', views.person_analysis_view, name='person_analysis'),
        path('analysis/channel/', views.channel_analysis_view, name='channel_analysis'),
        path('live_search/', views.LiveSearchView.as_view(), name='live_search'),
        path('person_details/<str:person_name>/', views.PersonDetailView.as_view(), name='person_details'),
        path('api/videos', views.VideoView.as_view(), name='video-list'),
        path('api/channels', views.ChannelView.as_view()),
        path('rss/', views.LatestPostsFeed(), name='post_feed'),




        path('blog/', views.Bloghome.as_view(), name='index'),  # use Bloghome view here
        path('blog/<str:blog_title>/', views.blog_post, name='blog-detail'),
        path('load-more-blogs/', views.load_more_blogs, name='load-more-blogs'),
        path('sitemap.xml', sitemap, {'sitemaps': sitemaps, 'template_name': 'pages/sitemap.xml'}, name='django.contrib.sitemaps.views.sitemap'),










         







         




        
]


urlpatterns += htmx_url_patterns