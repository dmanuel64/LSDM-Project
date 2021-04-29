from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from pymongo import MongoClient
from django.contrib.auth import authenticate,login, logout
from mysite.models import Post
import logging
logger = logging.getLogger(__name__)
# Create your views here.
def index(request):
    return render(request, 'index.html')
def load_database():
    server="localhost"
    port = 27017
    conn = MongoClient(server,port)
    print(conn)
def signup(request):
    username = request.POST.get('username')
    password = request.POST.get('passsword')
    user = authenticate(username=username, password=password)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index.html')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
def login_page(request):
    return render(request, 'login.html')
def forgot(request):
    return render(request, 'forgot-password.html')
def chart(request):
    return render(request, 'charts.html')
def tables(request):
    return render(request, 'tables.html')