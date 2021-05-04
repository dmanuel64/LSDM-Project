from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    username = models.TextField(),
    password = models.TextField()

class UserHistory(models.Model):
    search = models.CharField(max_length=280)
    sdate = models.DateTimeField(auto_now=True)
    related_user = models.ForeignKey(User, on_delete=models.CASCADE)

