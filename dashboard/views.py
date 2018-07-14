from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views import generic
from django.views.generic import View
from . forms import UserForm,SelectAccount, Watching_Accounts_Form
from .models import Social_Accounts,Watching_Accounts
import json
import time
import tweepy

import collections
import datetime
import calendar

from textblob import TextBlob
import requests

from django.views.generic.edit import CreateView, UpdateView, DeleteView

import twitter
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.error.TweepError:
            print("waiting 15 minutes for Twitter to let me get more tweets")
            time.sleep(15 * 60)

@login_required
def sentiment_result(value):
    if value > 0:
        return "positive"
    elif value < 0:
        return "negative"
    else:
        return "neutral"
# Create your views here.
# import authentication credentials

from .secrets import TWITTER_C_KEY, TWITTER_C_SECRET, TWITTER_A_KEY, TWITTER_A_SECRET

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(TWITTER_C_KEY, TWITTER_C_SECRET)
auth.set_access_token(TWITTER_A_KEY, TWITTER_A_SECRET)
api = tweepy.API(auth)

@login_required
def index(request):

    social_form = SelectAccount(request.POST or None)
    if social_form.is_valid():
        instance = social_form.save(commit=False)
        instance.user=request.user
        instance.save()
    # latest_account=get_object_or_404(Social_Accounts,latest='created_at')

    try:
        # try and get the related twitter object
        latest_account=Social_Accounts.objects.filter(user=request.user).latest('created_at')
        # if user object available, then get all tweets, sentiment and days posted from
        user_results = api.get_user(screen_name=latest_account.twitter_username)

        recent_tweets = api.user_timeline(screen_name=latest_account.twitter_username, count=200)

        tweets_classifier = api.user_timeline(screen_name=latest_account.twitter_username, since="2017-01-10",
                                              # point of time you want the search to end
                                              until="2017-03-10", )
        posts_per_month = []
        posts_per_day = []
        posts_per_year = []
        date_and_year = []
        days_posted_on = []
        polarity_values = []
        polarity_texts = []
        polarity_positive = 0
        polarity_negative = 0
        polarity_neutral = 0

        # sunday =1 , monday, so on
        number_of_day = []
        for recent_tweet in recent_tweets:
            try:
                created_at_year = str(recent_tweet.created_at)

                posts_per_year.append(created_at_year[0:4] + "\n")
                extracted_year_and_date = created_at_year[0:10]

                # tweet and date dictionary

                extracted_year_and_date = extracted_year_and_date.replace("-", "")
                extracted_year_and_date = datetime.datetime.strptime(extracted_year_and_date, "%Y%m%d").date()
                extracted_number_of_day = extracted_year_and_date.weekday()
                extracted_year_and_date = calendar.day_name[extracted_year_and_date.weekday()]

                days_posted_on.append(extracted_year_and_date)
                number_of_day.append(extracted_number_of_day)
                date_and_year.append(created_at_year[0:10])
                analysis = TextBlob(recent_tweet.text)
                polarity_value = analysis.sentiment.polarity

                polarity_values.append(polarity_value)
                # polarity_text = sentiment_result(analysis.sentiment.polarity)
                if polarity_value > 0:
                    polarity_text = "positive"
                elif polarity_value < 0:
                    polarity_text = "negative"
                else:
                    polarity_text = "neutral"

                if polarity_text == 'positive':
                    polarity_positive += 1
                elif polarity_text == 'neutral':
                    polarity_neutral += 1
                elif polarity_text == 'negative':
                    polarity_negative += 1

                polarity_texts.append(polarity_text)
                # print ( "posts_per_month:",{},"years:",{},len(created_at_year),len(created_at_year) )
            except tweepy.TweepError:
                time.sleep(15 * 60)

            except StopIteration:
                break

        days_posted_on = [x for _, x in sorted(zip(number_of_day, days_posted_on))]
        # analyze how often a person posts per day: which days are they most free?
        name_of_weekday = []
        posts_count_on_day = []
        posts_per_day_numbers = collections.Counter(days_posted_on)

        for sing_date in posts_per_day_numbers:
            name_of_weekday.append(sing_date)
            posts_count_on_day.append(posts_per_day_numbers[sing_date])

        # analyze the post dates
        date_and_year_numbers = collections.Counter(date_and_year)

        sentiment_per_day_numbers = collections.Counter(polarity_texts)
        post_on_date = []
        no_of_posts_on_date = []
        sentiment_of_posts_on_date = [len(recent_tweets)]

        for i in date_and_year_numbers:
            post_on_date.append(i)
            no_of_posts_on_date.append(str(date_and_year_numbers[i]))
            counter = 0



        context = {'page_title': 'Dashboard', 'user_results': user_results, 'recent_tweets': recent_tweets,
                   "post_on_date": post_on_date, "no_of_posts_on_date": no_of_posts_on_date,
                   "posts_count_on_day": posts_count_on_day, "name_of_weekday": name_of_weekday,
                   "polarity_values": polarity_values, "polarity_positive": polarity_positive
            , "polarity_neutral": polarity_neutral, "polarity_negative": polarity_negative, "social_form":social_form,"latest_account":latest_account}









    except:
        #if not found, redirect user to a page and let them select their default account
        term = request.user.username

        user_results = api.search_users(q=term)
        if term == '':
            message = 'Your username was not entered correctly.'
        else:
            message = term

        context = {'page_title': 'Select Default Account', 'term': term, 'message': message, 'user_results': user_results}
        return render(request, 'dashboard/select_account.html', context)



    return render(request, 'dashboard/index.html',context)



#this method allows the user to change the search term when selecting their default user account
@login_required
def change_seach_term(request):

    term=request.GET['search_term']

    user_results=api.search_users(q=term)
    if term=='':
        message = 'You submitted an empty form.'
    else:
        message=term

    context={'page_title':'user search results', 'term':term, 'message':message, 'user_results':user_results}

    return render(request, 'dashboard/select_account.html', context)

    # return HttpResponse(
    #     for user_results in user_results
    #     user_results.screen_name
    #     )

@login_required
def user_search(request):
    context={'page_title':'user search','post_action':'user_search_result','page_type':'Users'}
    return render(request, 'dashboard/user_search.html',context)
@login_required
def user_search_result(request):

    term=request.GET['search_term']

    user_results=api.search_users(q=term)
    if term=='':
        message = 'You submitted an empty form.'
    else:
        message=term
    users_watching = Watching_Accounts.objects.filter(user=request.user)
    context={'page_title':'user search results', 'term':term, 'message':message, 'user_results':user_results,'users_watching':users_watching }

    return render(request, 'dashboard/user_search_result.html', context)



# render topic search page

@login_required
def topic_search(request):
    context={'page_title':'Topic search', 'page_type':'Topics','post_action':'topic_search_result'}
    return render(request, 'dashboard/user_search.html',context)

# return search result
@login_required
def topic_search_result(request):
    term = request.GET['search_term']

    recent_tweets = api.search(q=term,since="",rpp=100)
    if term == '':
        message = 'You submitted an empty form.'
    else:
        message = term

    context = {'page_title': 'user search results', 'term': term, 'message': message, 'recent_tweets': recent_tweets}

    #return HttpResponse(recent_tweets)
    return render(request, 'dashboard/topic_search_result.html', context)


@login_required
def single_user_tweets(request,user_name):
    user_results = api.get_user(screen_name=user_name)


    recent_tweets = api.user_timeline(screen_name=user_name, count=200)

    tweets_classifier=api.user_timeline(screen_name=user_name,since="2017-01-10",
                    # point of time you want the search to end
                    until="2017-03-10",)
    posts_per_month=[]
    posts_per_day=[]
    posts_per_year=[]
    date_and_year=[]
    days_posted_on=[]
    polarity_values=[]
    polarity_texts=[]
    polarity_positive=0
    polarity_negative=0
    polarity_neutral=0

    #sunday =1 , monday, so on
    number_of_day=[]
    for recent_tweet in recent_tweets:
        try:
            created_at_year=str(recent_tweet.created_at)


            posts_per_year.append(created_at_year[0:4] + "\n")
            extracted_year_and_date=created_at_year[0:10]

            #tweet and date dictionary

            extracted_year_and_date=extracted_year_and_date.replace("-", "")
            extracted_year_and_date=datetime.datetime.strptime(extracted_year_and_date, "%Y%m%d").date()
            extracted_number_of_day =extracted_year_and_date.weekday()
            extracted_year_and_date=calendar.day_name[extracted_year_and_date.weekday()]

            days_posted_on.append(extracted_year_and_date)
            number_of_day.append(extracted_number_of_day)
            date_and_year.append(created_at_year[0:10])
            analysis = TextBlob(recent_tweet.text)
            polarity_value= analysis.sentiment.polarity


            polarity_values.append(polarity_value)
            # polarity_text = sentiment_result(analysis.sentiment.polarity)
            if polarity_value > 0:
                polarity_text= "positive"
            elif polarity_value < 0:
                polarity_text= "negative"
            else:
                polarity_text= "neutral"

            if polarity_text == 'positive':
                polarity_positive+=1
            elif polarity_text == 'neutral':
                polarity_neutral+=1
            elif polarity_text=='negative':
                polarity_negative+=1


            polarity_texts.append(polarity_text)
            #print ( "posts_per_month:",{},"years:",{},len(created_at_year),len(created_at_year) )
        except tweepy.TweepError:
            time.sleep(15*60)

        except StopIteration:
            break

    days_posted_on = [x for _, x in sorted(zip(number_of_day, days_posted_on))]
    #analyze how often a person posts per day: which days are they most free?
    name_of_weekday=[]
    posts_count_on_day=[]
    posts_per_day_numbers=collections.Counter(days_posted_on)

    for sing_date in posts_per_day_numbers:
        name_of_weekday.append(sing_date)
        posts_count_on_day.append(posts_per_day_numbers[sing_date])



    #analyze the post dates
    date_and_year_numbers=collections.Counter(date_and_year)

    sentiment_per_day_numbers = collections.Counter(polarity_texts)
    post_on_date=[]
    no_of_posts_on_date=[]
    sentiment_of_posts_on_date=[len(recent_tweets)]

    for i in date_and_year_numbers:
        post_on_date.append(i)
        no_of_posts_on_date.append(str(date_and_year_numbers[i]))
        counter = 0




    context={'page_title':'Single User', 'user_results':user_results, 'recent_tweets':recent_tweets,"post_on_date":post_on_date, "no_of_posts_on_date":no_of_posts_on_date,"posts_count_on_day":posts_count_on_day,"name_of_weekday":name_of_weekday,"polarity_values": polarity_values,"polarity_positive":polarity_positive
,"polarity_neutral":polarity_neutral,"polarity_negative":polarity_negative}
    return render(request, 'dashboard/single_user.html',context)


@login_required
def trends(request):
    trend_locations=api.trends_available()
    # trend_locations=json.dumps(trend_locations)
    locations=[len(trend_locations)]
    count=0
    #get_pace_id=requests.get("http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.places%20where%20text%3D%22nairobi%20kenya%22&format=json").json()
    get_pace_id=requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=nairobi,+CA&key="+"AIzaSyA0xRTz67wxctfMn380M1Wd_CAkluttXWw").json()
    place_lats=[len(trend_locations)]
    #trend_in_city=api.trends_place(id=get_pace_id.query.results.place[1].woeid)
    #trends_near_me=api.trends_closest()

    # for place in trend_locations:
    #     locations.append(place)
    #     count += 1
        # place_lat=requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+locations[count]+",+CA&key="+"AIzaSyA0xRTz67wxctfMn380M1Wd_CAkluttXWw").json()
        # place_lats.append(place_lat)
        # print(place.name)
    one=1
    # locations=json.dump(locations)
    # print(len(locations))

    context = {'page_title': 'trends', 'trend_locations': trend_locations}

    return render(request, 'dashboard/trends.html',context)

@login_required
def single_place_trend(request,woe_id):


    trend_in_city=api.trends_place(id=woe_id)
    # trend_in_city=json.dumps(trend_in_city)
    context = {'page_title': 'single trend', 'woe_id': woe_id,'trend_in_city':trend_in_city}
    # return (woe_id)
    # return JsonResponse(trend_in_city)
    # return HttpResponse(json.dumps(trend_in_city), content_type="application/json")

    return render(request, 'dashboard/single_place_trend.html', context)

@login_required
def single_trend(request):
    trend_name = request.GET['trend_name']

    trend_search = api.search(q=trend_name)
    # trend_search=json.load(trend_search)
    if trend_name == '':
        message = 'You submitted an empty form.'
    else:
        message = trend_search

    context={'page_title':'Single Trend','trend_search':trend_search, 'message':message, 'trend_name':trend_name}
    return render(request, 'dashboard/single_trend.html',context)
    # return JsonResponse(trend_search)
    # return HttpResponse(trend_search)
    # return HttpResponse(json.dumps(trend_search), content_type="application/json")

@login_required
def mentions(request,):
    context={'page_title':'mentions'}
    return render(request, 'dashboard/mentions.html',context)


# @login_required
# def add_to_watch(request):
#     social_form = Watching_Accounts_Form(request.POST or None)
#     if social_form.is_valid():
#         instance = social_form.save(commit=False)
#         instance.user = request.user
#         instance.save()
#     return redirect('/dashboard/watch')
#     # latest_account=get_object_or_404(Social_Accounts,latest='created_at')

@login_required
def watch(request):
    social_form = Watching_Accounts_Form(request.POST or None)
    if social_form.is_valid():
        instance = social_form.save(commit=False)
        instance.user = request.user
        instance.save()
    else:
        pass
    users_watching = Watching_Accounts.objects.filter(user=request.user)
    context={'page_title':'watch','users_watching':users_watching}
    # return HttpResponse(users_watching)
    return render(request, 'dashboard/watch.html',context)

@login_required
def watch_single(request,id):

    context={'page_title':'watch'+id , }
    # return HttpResponse(users_watching)
    return render(request, 'dashboard/watch_single.html',context)

@login_required
def companies(request):
    context={'page_title':'companies'}
    return render(request, 'dashboard/companies.html',context)
@login_required
def users(request):
    context={'page_title':'users'}
    return render(request, 'dashboard/users.html',context)

@login_required
def support(request):
    context={'page_title':'support'}
    return render(request, 'dashboard/support.html',context)
@login_required
def events(request):
    context={'page_title':'events'}
    return render(request, 'dashboard/events.html',context)
@login_required
def events_single(request, id):
    context={'page_title':'events'+id}
    return render(request, 'dashboard/events_single.html',context)



