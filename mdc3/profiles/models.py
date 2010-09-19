from django.db import models
from django.contrib.auth.models import User

##class Profile(models.Model):
##    #data
##    id = models.ForeignKey(User,null=False)
##    ip_signup = models.IPAddressField()
##    new_message = models.BooleanField()
##    last_login = models.DateTimeField()
##    last_view = models.DateTimeField()
##    last_post = models.DateTimeField()
##    last_profile_update = models.DateTimeField()
##    profile_views = models.IntegerField()
##    last_events_view = models.DateTimeField()
##    banned = models.BooleanField(default=False)
##    #info
##    zip_code = models.CharField(max_lenth=50)
##    city = models.CharField(max_lenth=50)
##    location = models.CharField(max_lenth=50)
##    aim_name = models.CharField(max_lenth=50)
##    gchat_name = models.CharField(max_lenth=50)
##    website = models.URLField(max_lenth=150)
##    info = models.CharField(max_lenth=2500)
##    #preferences
##    email_public = models.BooleanField(default=False)
##    security_answer = models.CharField(max_length=32)
##    show_images = models.BooleanField(default=True)
##    #fuck hidden
##    photo_url = models.URLField()
##
##    def __str__(self):
##        return self.id.username
    
    
