from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from bbcode.fields import BBCodeTextField
import datetime


class PM(models.Model):
    subject = models.CharField(max_length=100, blank=False)
    body = BBCodeTextField(default='')
    sender = models.ForeignKey(User, related_name='sent_pms',
                               default="(no subject)")
    recipients = models.ManyToManyField(User,
            related_name='recieved_pms',
            through='Recipient')
    created_on = models.DateTimeField(default=datetime.datetime.now)
    parent = models.ForeignKey('self',null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    #there is clearly a one line query for this but this will
    #work for now
    def get_rec_str(self):
        rec_list = Recipient.objects.filter(message=self)
        rec_str =''
        for rec in rec_list:
            rec_str += rec.recipient.username + ' '
        return rec_str
        


class Recipient(models.Model):
    recipient = models.ForeignKey(User)
    message = models.ForeignKey(PM)
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.recipient.username


def clear_pm_count(sender, instance, signal, *args, **kwargs):
    cache_key = "pm-count:%d:%d"%(
        Site.objects.get_current().id,
        instance.recipient.id,
    )
    cache.delete(cache_key)
   
post_save.connect(clear_pm_count, sender=Recipient)
