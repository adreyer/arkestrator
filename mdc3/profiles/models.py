import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from mdc3.invites.models import Invite
from mdc3.events.models import Market




class Profile(models.Model):
    #data
    user = models.OneToOneField(User,null=False)
    ip_signup = models.IPAddressField()
    last_login = models.DateTimeField(default=datetime.datetime.now)
    last_view = models.DateTimeField(default=datetime.datetime.now)
    last_post = models.DateTimeField(default=datetime.datetime.now)
    last_profile_update = models.DateTimeField(default=datetime.datetime.now)
    profile_views = models.IntegerField(default=0)
    last_events_view = models.DateTimeField(default=datetime.datetime.now)
    invite_used = models.ForeignKey(Invite, null=True)
    
    
    #info
    name = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, blank=True)
    aim_name = models.CharField(max_length=50, blank=True)
    gtalk_name = models.CharField(max_length=50, blank=True)
    email_public = models.EmailField(blank=True)
    website = models.URLField(max_length=150, blank=True)
    info = models.TextField(blank=True)
    photo_url = models.URLField(blank=True)
    phone = models.CharField(max_length=50,blank=True)
    
    #preferences
    show_images = models.BooleanField(default=True)
    collapse_size = models.IntegerField(default=10)
    market = models.ForeignKey(Market,null=True)
    #fuck hidden
    
    
    def get_absolute_url(self):
        return reverse('view-profile', kwargs={'user_id' : self.user.id})
    
    def __str__(self):
        return self.user.username

    def total_posts(self):
        return self.user.post_set.count()

    def total_threads(self):
        return self.user.threads.count()

    def last_seen(self):
        from mdc3.board.models import LastRead
        lr = LastRead.objects.filter(user=self.user).order_by(
                '-timestamp')
        if lr:
            return lr[0].timestamp
        return self.user.date_joined
