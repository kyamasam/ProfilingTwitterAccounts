from django.contrib.auth.models import User
from .models import Social_Accounts ,Watching_Accounts
from django import forms
from django.forms import ModelForm

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model= User
        fields=['username','email', 'password']



class SelectAccount(forms.ModelForm):
    twitter_username = forms.CharField()
    class Meta:
        model = Social_Accounts
        fields = ['twitter_username', ]

class Watching_Accounts_Form(forms.ModelForm):
    twitter_username = forms.CharField()
    twitter_profile_pic=forms.CharField()
    verified=forms.BooleanField()
    class Meta:
        model = Watching_Accounts
        # this field belongs to the user we are watching
        fields=['twitter_username', 'twitter_profile_pic','verified']