from django.db import models
from django.conf   import settings
# from django.core.urlresolvers
# Create your models here.


class Social_Accounts(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name="social_accounts")
    twitter_username=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Watching_Accounts(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_watched_by")
    # belongs to the user we are watching
    twitter_username=models.CharField(max_length=250)
    verified=models.BooleanField(default=False)
    twitter_profile_pic=models.CharField(max_length=250, default='https://x1.xingassets.com/assets/frontend_minified/img/users/nobody_m.original.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


