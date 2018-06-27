from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index ,name='index'),

    url(r'trends/', views.trends, name='trends'),
    url(r'user_search/', views.user_search, name='user_search'),
    url(r'user_search_result/$', views.user_search_result, name='user_search_result'),
    url(r'^mentions/$', views.mentions, name='mentions'),
    url(r'single_user/(?P<user_name>[\w\-]+)/$', views.single_user, name='single_user'),
    url(r'watch/$', views.watch, name='watch'),
    url(r'watch/(?P<id>\d+)/$', views.watch_single, name='watch_single'),
    url(r'companies/', views.companies, name='companies'),
    url(r'users/', views.users, name='users'),
    url(r'support/', views.support, name='support'),
    url(r'events/$', views.events, name='events'),
    url(r'events/(?P<id>\d+)/$', views.events_single, name='events_single'),
    # url(r'^details/(?P<id>\d+)/$', views.details ,name='details')

]