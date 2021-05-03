from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from pymongo import MongoClient
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from mysite.models import Post
from pythonScripts import twitterCollection
from pythonScripts import googletrends
import simplejson as json
from mysite import visualization

import logging
logger = logging.getLogger(__name__)
# Create your views here

#Render main page
def index(request):
    return render(request, 'index.html')

#Handle a search request
def search(request):
    if request.method == 'POST':
        #Get the requested search term and load the respective data
        get_text = request.POST.get('searchInput')
        twitterCollection.twitter(get_text)
        googletrends.google(get_text)
    return render(request, 'index.html')


def load_database():
    server="localhost"
    port = 27017
    conn = MongoClient(server,port)
    print(conn)

# Handle user signing up for an account
def signup(request):
    # If the method is a post, create an account from the user's information
    if request.method == 'POST':
        # Get the input form
        form = UserCreationForm(request.POST)
        #Create the account and log in if the form is valid
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            new_user = User.objects.create_user(username, username, raw_password)
            new_user.save()
            login(request, new_user)
            # At this point the user has been created and is logged in, so redirect back to the home page
            return redirect('/')
    # Display the registration page otherwise
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Handle user logging in to the website
def login_page(request):
    # Only show the page if the user is not already logged in
    if not request.user.is_authenticated:
        # Handle the login request
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=username, password=upass)
                if user is not None:
                    login(request, user)
                    return redirect('/')
        # Display the login form if a login request hasn't been made yet
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    else:
        return redirect('/')


def forgot(request):
    return render(request, 'forgot-password.html')


def tweet_chart(request):
    bar = visualization.Bar()

    results = bar.tweets_bar()
    bar_labels = results[0]
    bar_data = results[1]
    
    results = bar.per_day()
    bar2_labels = results[0]
    bar2_data = results[1]

    results = bar.monthly_tweets()
    line_labels = results[0]
    line_data = results[1]
    
    all_data = {"line_labels": line_labels,"line_data": line_data, "bar_labels": bar_labels, "bar_data":bar_data, 
                    "bar2_labels": bar2_labels, "bar2_data":bar2_data }

    return render(request, 'tweet-charts.html', all_data)

def hashtags_chart(request):
    pie = visualization.Pie()
    bar = visualization.Bar()

    results = pie.top_pie(5, "hashtags")
    pie_labels = results[0]
    pie_data = results[1]

    results = bar.top_hashtag(5)
    bar_labels = results[0]
    bar_data = results[1]    

    results = bar.hashtag_retweet(5)
    bar2_labels = results[0]
    bar2_data = results[1]
    
    results = bar.hashtag_favorite(5)
    bar3_labels = results[0]
    bar3_data = results[1]

    all_data = {"pie_labels":pie_labels, "pie_data":pie_data, "bar_labels": bar_labels,"bar_data": bar_data,
                    "bar2_labels": bar2_labels, "bar2_data":bar2_data, "bar3_labels": bar3_labels, "bar3_data":bar3_data}

    return render(request, 'hashtags-charts.html', all_data)

def engagement_chart(request):
    bar = visualization.Bar()
    line = visualization.Line()

    results = line.month_engagement()
    line_labels = results[0]
    line_data = results[1]    

    results = bar.daily_engagement("total_engagement")
    bar_labels = results[0]
    bar_data = results[1]

    results = bar.daily_engagement("retweets")
    bar2_labels = results[0]
    bar2_data = results[1]

    results = bar.daily_engagement("favorites")
    bar3_labels = results[0]
    bar3_data = results[1]

    all_data = {"line_labels":line_labels, "line_data":line_data, "bar_labels": bar_labels, "bar_data":bar_data,
                    "bar2_labels": bar2_labels, "bar2_data":bar2_data, "bar3_labels": bar3_labels, "bar3_data":bar3_data}

    return render(request, 'engagement-charts.html', all_data)

def source_chart(request):
    bar = visualization.Bar()
    pie = visualization.Pie()

    results = pie.top_pie(5, "source")
    pie_labels = results[0]
    pie_data = results[1] 

    results = pie.top_pie(5, "user_location")
    pie2_labels = results[0]
    pie2_data = results[1] 

    results = bar.source_max(5)
    bar_labels = results[0]
    bar_data = results[1] 

    results = bar.top_location(5)
    bar2_labels = results[0]
    bar2_data = results[1]     

    all_data = {"pie_labels":pie_labels, "pie_data":pie_data, "pie2_labels":pie2_labels, "pie2_data":pie2_data,
                    "bar_labels": bar_labels, "bar_data":bar_data, "bar2_labels": bar2_labels, "bar2_data":bar2_data }

    return render(request, 'source-charts.html', all_data)    

def account_chart(request):
    bar = visualization.Bar()
    pie = visualization.Pie()

    results = pie.verified_pie()
    pie_labels = results[0]
    pie_data = results[1] 

    results = bar.verified_bar()
    bar_labels = results[0]
    bar_data = results[1] 

    results = bar.user_engagement_bar("total_engagement")
    bar1_labels = results[0]
    bar1_data = results[1]

    results = bar.user_engagement_bar("retweets")
    bar2_labels = results[0]
    bar2_data = results[1]

    results = bar.user_engagement_bar("favorites")
    bar3_labels = results[0]
    bar3_data = results[1]

    all_data = {"pie_labels":pie_labels, "pie_data":pie_data, "bar_labels": bar_labels, "bar_data":bar_data,
                    "bar1_labels": bar1_labels, "bar1_data":bar1_data,"bar2_labels": bar2_labels, "bar2_data":bar2_data,
                        "bar3_labels": bar3_labels, "bar3_data":bar3_data}

    return render(request, 'account-charts.html', all_data)   

def tables(request):
    return render(request, 'tables.html')