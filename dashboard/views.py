from django.shortcuts import render
from django.http import HttpResponse
import json
import time
import tweepy

import collections
import datetime
import calendar

from textblob import TextBlob


def sentiment_result(value):
    if value >0:
        return "positive"
    elif value <0 :
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

def index(request):
    context={'page_title':'Dashboard'}
    return render(request, 'dashboard/index.html',context)

def user_search(request):
    context={'page_title':'user search'}
    return render(request, 'dashboard/user_search.html',context)

def user_search_result(request):

    term=request.GET['search_term']

    user_results=api.search_users(q=term)
    if term=='':
        message = 'You submitted an empty form.'
    else:
        message=term

    context={'page_title':'user search results', 'term':term, 'message':message, 'user_results':user_results}

    return render(request, 'dashboard/user_search_result.html', context)

    # return HttpResponse(
    #     for user_results in user_results
    #     user_results.screen_name
    #     )
def single_user(request,user_name):
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
            polarity_text= sentiment_result(analysis.sentiment.polarity)
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




    #return HttpResponse(json.dumps({"dayname":name_of_weekday, "no_of_posts_on_date":posts_count_on_day }),content_type="application/json" )

    #return HttpResponse(json.dumps({"sentiment": sentiment_per_day_numbers, "count":len(polarity_texts)}), content_type="application/json")
    context={'page_title':'Single User', 'user_results':user_results, 'recent_tweets':recent_tweets,"post_on_date":post_on_date, "no_of_posts_on_date":no_of_posts_on_date,"posts_count_on_day":posts_count_on_day,"name_of_weekday":name_of_weekday,"polarity_values": polarity_values,"polarity_texts":polarity_texts }
    return render(request, 'dashboard/single_user.html',context)

def trends(request):
    context={'page_title':'trends'}
    return render(request, 'dashboard/trends.html',context)
def mentions(request):
    context={'page_title':'mentions'}
    return render(request, 'dashboard/mentions.html',context)

def watch(request):
    context={'page_title':'watch'}
    return render(request, 'dashboard/watch.html',context)

def watch_single(request,id):
    context={'page_title':'watch'+id}
    return render(request, 'dashboard/watch_single.html',context)

def companies(request):
    context={'page_title':'companies'}
    return render(request, 'dashboard/companies.html',context)
def users(request):
    context={'page_title':'users'}
    return render(request, 'dashboard/users.html',context)

def support(request):
    context={'page_title':'support'}
    return render(request, 'dashboard/support.html',context)
def events(request):
    context={'page_title':'events'}
    return render(request, 'dashboard/events.html',context)
def events_single(request, id):
    context={'page_title':'events'+id}
    return render(request, 'dashboard/events_single.html',context)