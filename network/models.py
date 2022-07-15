from datetime import datetime
from email import message
from msilib.schema import SelfReg
from operator import mod
from pickle import TRUE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers")

    def getfollowerscount(self):
        return self.followers.count()
    def getfollowingcount(self):
        return self.following.count()
    def isfollowingx(self, x):
        return x in self.following.all()

class Post(models.Model):
    message = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(User, related_name="likedposts")
    datetime = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)

    def getlikescount(self):
        return f"{self.likes.count()}"
    def getdatetime(self):
        return self.datetime.strftime('%B %d, %Y %I:%M %p')
