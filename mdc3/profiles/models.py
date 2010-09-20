from django.db import models
from django.contrib.auth.models import User
from mdc3.invites.models import Invite

import datetime

class Profile(models.Model):
    #data
    user = models.OneToOneField(User,null=False)
    ip_signup = models.IPAddressField()
    new_message = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=datetime.datetime.now)
    last_view = models.DateTimeField(default=datetime.datetime.now)
    last_post = models.DateTimeField(default=datetime.datetime.now)
    last_profile_update = models.DateTimeField(default=datetime.datetime.now)
    profile_views = models.IntegerField(default=0)
    last_events_view = models.DateTimeField(default=datetime.datetime.now)
    banned = models.BooleanField(default=False)
    invite_used = models.ForeignKey(Invite, null=True)
    #info
    name = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, blank=True)
    aim_name = models.CharField(max_length=50, blank=True)
    gtalk_name = models.CharField(max_length=50, blank=True)
    website = models.URLField(max_length=150, blank=True)
    info = models.CharField(max_length=2500, blank=True)
    email_public = models.EmailField(blank=True)
    #preferences
    show_images = models.BooleanField(default=True)
    #fuck hidden
    photo_url = models.URLField(blank=True)
    

    def __str__(self):
        return self.user.username
    
    
