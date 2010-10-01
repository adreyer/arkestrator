from django.db import models
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

    def __str__(self):
        return self.recipient.username
