from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from pymongo import MongoClient
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from mysite.models import Post
from pythonScripts import twitterCollection
from pythonScripts import googletrends
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


def chart(request):
    return render(request, 'charts.html')


def tables(request):
    return render(request, 'tables.html')