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
# Create your views here.
def index(request):
    return render(request, 'index.html')
def search(request):
    if request.method == 'POST':
        get_text = request.POST.get('searchInput')
        twitterCollection.twitter(get_text)
        googletrends.google(get_text)
    return render(request, 'index.html')
def load_database():
    server="localhost"
    port = 27017
    conn = MongoClient(server,port)
    print(conn)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            new_user = User.objects.create_user(username, username, raw_password)
            new_user.save()
            login(request, new_user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
def login_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=username, password=upass)
                if user is not None:
                    login(request, user)
                    return redirect('/')
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