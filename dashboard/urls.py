from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index ,name='spider_dashboard'),

    url(r'trends/', views.trends, name='trends'),
    url(r'single_place_trend/(?P<woe_id>\d+)/$', views.single_place_trend, name='single_place_trend'),
    url(r'single_trend/(?P<trend_name>[\w\-]+)/$', views.single_trend, name='single_trend'),
    url(r'single_trend/$', views.single_trend, name='single_trend'),
    url(r'user_search/', views.user_search, name='user_search'),
    url(r'change_seach_term/', views.change_seach_term, name='change_seach_term'),
    url(r'user_search_result/$', views.user_search_result, name='user_search_result'),

    # topic search

    url(r'topic_search/', views.topic_search, name='change_seach_term'),
    url(r'topic_search_result/$', views.topic_search_result, name='user_search_result'),

    url(r'^mentions/$', views.mentions, name='mentions'),
    url(r'single_user/(?P<user_name>[\w\-]+)/$', views.single_user_tweets, name='single_user'),
    url(r'watch/', views.watch, name='watch'),
    url(r'watch/(?P<id>\d+)/$', views.watch_single, name='watch_single'),
    url(r'companies/', views.companies, name='companies'),
    url(r'users/', views.users, name='users'),
    url(r'support/', views.support, name='support'),
    url(r'events/$', views.events, name='events'),
    url(r'events/(?P<id>\d+)/$', views.events_single, name='events_single'),

    # registration
    # url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # url(r'^details/(?P<id>\d+)/$', views.details ,name='details')

]