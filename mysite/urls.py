"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from mysite import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('search/', views.search, name="search"),
    path('login/', views.login_page, name="login"),
    path('', views.load_database, name="load_database"),
    path('register/', views.signup, name="register"),
    path('forgot-password/', views.forgot, name="forgot-password"),
    path('tweet-charts/', views.tweet_chart,name="tweet-charts"),
    path('hashtags-charts/', views.hashtags_chart,name="hashtags-charts"),
    path('engagement-charts/', views.engagement_chart,name="engagement-charts"),
    path('account-charts/', views.account_chart,name="account-charts"),
    path('source-charts/', views.source_chart,name="source-charts"),
    path('sentiment-charts/', views.sentiment_chart,name="sentiment-charts"),    
    path('sentimental-analysis/', views.sentimental_analysis,name="sentimental-analysis"),        
    path('charts/', views.tweet_chart,name="charts"),
    path('tables/', views.tables,name="tables"),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.user_profile, name='user-profile'),
    path('google-trends/', views.google_trends,name="google-trends")
]
