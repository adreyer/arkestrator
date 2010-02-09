from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

class Thread(models.Model):
    title = models.CharField(max_length=60, blank=False)
    
    site = models.ForeignKey(Site, null=False)
    on_site = CurrentSiteManager()

    def __str__(self):
        return self.title

class Post(models.Model):
    thread = models.ForeignKey(Thread, null=False)
    
    body = models.TextField(blank=False)
    
    def __str__(self):
        return "%s: %s"%(str(self.thread),self.body[:20])

