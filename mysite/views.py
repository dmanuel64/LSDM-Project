from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    return render(request, 'index.html')
def signup(request):
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
def login(request):
    return render(request, 'login.html')
def forgot(request):
    return render(request, 'forgot-password.html')
def chart(request):
    return render(request, 'charts.html')
def tables(request):
    return render(request, 'tables.html')