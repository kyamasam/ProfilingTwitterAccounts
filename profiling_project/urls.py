"""profiling_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.core, name='core')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='core')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views as core_views


from django.conf.urls.static import settings,static

urlpatterns = [
    url(r'^$', core_views.index, name="index"),
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^accounts/signup/$', core_views.signup, name='signup'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^accounts/password_change/$', auth_views.password_change, name='password_change'),
    url(r'^accounts/password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^accounts/password_reset/done/$', auth_views.password_reset, name='password_reset_done'),
    url(r'^accounts/reset/<uidb64>/<token>/$', auth_views.password_reset_confirm ,name='password_reset_confirm'),
    url(r'^accounts/reset/done/$',auth_views.password_reset_complete, name='password_reset_complete'),
    # url(r'^auth/social/', core_views.home, name='social')),
    url(r'auth/social/', include('social_django.urls', namespace='social')),
    # url(r'^login/$', auth_views.login, name='login'),
    # url(r'^logout/$', auth_views.logout, name='logout'),

    # url(r'^admin/', admin.site.urls),


]


if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT);
