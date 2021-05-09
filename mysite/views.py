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
from mysite import visualization, table, googleTrends
from .models import UserHistory

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
        twitter = twitterCollection.twitter(get_text)
        google = googletrends.google(get_text)
        context={
            'location': google,
            'reUser': twitter[0],
            'popUser': twitter[1],
        }
    return render(request, 'index.html', context)


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

def user_profile(request):
    if request.user.is_authenticated:
        history = UserHistory.objects.filter(related_user=request.user)
        context = {'user': request.user, 'history': history}
        return render(request, 'profile.html', context)
    else:
        return redirect('/')

def tweet_chart(request):
    bar = visualization.Bar()

    bar_labels, bar_data = bar.tweets_bar()
    bar2_labels, bar2_data = bar.per_day()
    line_labels, line_data = bar.monthly_tweets()
    
    all_data = {"line_labels": line_labels,"line_data": line_data, "bar_labels": bar_labels, "bar_data":bar_data, 
                    "bar2_labels": bar2_labels, "bar2_data":bar2_data }

    return render(request, 'tweet-charts.html', all_data)

def hashtags_chart(request):
    pie = visualization.Pie()
    bar = visualization.Bar()

    pie_labels, pie_data = pie.top_pie(5, "hashtags")
    bar_labels, bar_data = bar.top_hashtag(5)
    bar2_labels, bar2_data = bar.hashtag_retweet_favorite("retweets", 5)
    bar3_labels, bar3_data = bar.hashtag_retweet_favorite("favorites", 5)

    all_data = {"pie_labels":pie_labels, "pie_data":pie_data, "bar_labels": bar_labels,"bar_data": bar_data,
                    "bar2_labels": bar2_labels, "bar2_data":bar2_data, "bar3_labels": bar3_labels, "bar3_data":bar3_data}

    return render(request, 'hashtags-charts.html', all_data)

def engagement_chart(request):
    bar = visualization.Bar()
    line = visualization.Line()

    line_labels, line_data = line.month_engagement()    
    bar_labels, bar_data = bar.daily_engagement("total_engagement")
    bar2_labels, bar2_data = bar.daily_engagement("retweets")
    bar3_labels, bar3_data = bar.daily_engagement("favorites")

    all_data = {"line_labels":line_labels, "line_data":line_data, "bar_labels": bar_labels, "bar_data":bar_data,
                    "bar2_labels": bar2_labels, "bar2_data":bar2_data, "bar3_labels": bar3_labels, "bar3_data":bar3_data}

    return render(request, 'engagement-charts.html', all_data)

def sentiment_chart(request):
    pie = visualization.Pie()
    sentiment = visualization.Sentiment()

    pie_labels, pie_data = pie.sentiment_pie()
    bar_labels, bar_data = sentiment.accounts_sentiment("positive", 10)
    bar2_labels, bar2_data = sentiment.accounts_sentiment("neutral", 10)
    bar3_labels, bar3_data = sentiment.accounts_sentiment("negative",10)
    bar4_labels, bar4_data = sentiment.sentiment_bar()
    line_labels, line_data = sentiment.sentiment_date("positive")
    line2_labels, line2_data = sentiment.sentiment_date("neutral")
    line3_labels, line3_data = sentiment.sentiment_date("negative")

    all_data = {"pie_labels":pie_labels, "pie_data":pie_data, 
                    "bar_labels": bar_labels, "bar_data":bar_data, "bar2_labels": bar2_labels, "bar2_data":bar2_data, 
                    "bar3_labels": bar3_labels, "bar3_data":bar3_data, "bar4_labels": bar4_labels, "bar4_data":bar4_data, 
                        "line_labels": line_labels,"line_data": line_data, "line2_labels": line2_labels,"line2_data": line2_data,
                            "line3_labels": line3_labels,"line3_data": line3_data}

    return render(request, 'sentiment-charts.html', all_data)    

def source_chart(request):
    bar = visualization.Bar()
    pie = visualization.Pie()

    pie_labels, pie_data = pie.top_pie(5, "source")
    pie2_labels, pie2_data = pie.top_pie(5, "user_location")
    bar_labels, bar_data = bar.source_max(5)
    bar2_labels, bar2_data = bar.top_location(5)  

    all_data = {"pie_labels":pie_labels, "pie_data":pie_data, "pie2_labels":pie2_labels, "pie2_data":pie2_data,
                    "bar_labels": bar_labels, "bar_data":bar_data, "bar2_labels": bar2_labels, "bar2_data":bar2_data }

    return render(request, 'source-charts.html', all_data)    

def account_chart(request):
    bar = visualization.Bar()
    pie = visualization.Pie()

    pie_labels, pie_data = pie.verified_pie()
    bar_labels, bar_data = bar.verified_bar()
    bar1_labels, bar1_data = bar.user_engagement_bar("total_engagement")
    bar2_labels, bar2_data = bar.user_engagement_bar("retweets")
    bar3_labels, bar3_data = bar.user_engagement_bar("favorites")

    all_data = {"pie_labels":pie_labels, "pie_data":pie_data, "bar_labels": bar_labels, "bar_data":bar_data,
                    "bar1_labels": bar1_labels, "bar1_data":bar1_data,"bar2_labels": bar2_labels, "bar2_data":bar2_data,
                        "bar3_labels": bar3_labels, "bar3_data":bar3_data}

    return render(request, 'account-charts.html', all_data)   

def tables(request):
    tab = table.Table()
    data = []
    search = ""

    if request.GET:
        search = request.GET['search']
        if request.user.is_authenticated:
            UserHistory.objects.create(search=search, related_user=request.user)
        results = tab.search(search)
        json_records = results.reset_index().to_json(orient ='records') 
    else:
        results = tab.search("")
        json_records = results.reset_index().to_json(orient ='records')

    data = json.loads(json_records)
    context = {'d':data, 'search_item': search}    
    
    return render(request, 'tables.html', context)

def sentimental_analysis(request):
    tab = table.Table()

    if request.GET:
        input_sent = request.GET
        polarity, subjectivity = tab.input_sentimental(input_sent)
        print(polarity, subjectivity)
    else:
        results = tab.top_polarity("positive", 10)  
        json_records = results.reset_index().to_json(orient ='records')
        pos_data = json.loads(json_records)

        results = tab.top_polarity("negative", 10)  
        json_records = results.reset_index().to_json(orient ='records')   
        neg_data = json.loads(json_records)

        results = tab.top_subjectivity("objective", 10)  
        json_records = results.reset_index().to_json(orient ='records')   
        sub_data = json.loads(json_records)

        results = tab.top_subjectivity("subjective", 10)  
        json_records = results.reset_index().to_json(orient ='records')   
        obj_data = json.loads(json_records)        

    context = {'pos_data':pos_data,'neg_data':neg_data,
                    'sub_data':sub_data, 'obj_data': obj_data}      
     
    
    return render(request, 'sentimental-analysis.html', context) 

def google_trends(request):
    line = googleTrends.Line()
    bar = googleTrends.Bar()

    line_labels, line_data = line.google_line('covid')
    bar_labels, bar_data = bar.google_bar('pfizer')
    bar2_labels, bar2_data = bar.google_bar('moderna')
    bar3_labels, bar3_data = bar.google_bar('J&J Vaccine')
    
    all_data = {"line_labels": line_labels,"line_data": line_data, "bar_labels": bar_labels, "bar_data":bar_data,
                    "bar2_labels": bar2_labels, "bar2_data":bar2_data, "bar3_labels": bar3_labels, "bar3_data":bar3_data}
    
    return render(request, 'google-trends.html', all_data)    
