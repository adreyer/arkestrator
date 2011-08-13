from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
import datetime

from bbking.fields import BBCodeField

class PM(models.Model):
    """ a private message

        subject: subject
        body:   body
        sender: sender
        recipients: recipients
        parent:  the pm this pm is reply to or null
        root_parent: the original pm in this thread of replies
        created_at: when the pm was created
        deleted:  True if the sender has deleted this
        bbcode:   the bbcode body
    """

    subject = models.CharField(max_length=100, blank=False)
    body = models.TextField(default='')
    sender = models.ForeignKey(User, related_name='sent_pms',
                               default="(no subject)")
    recipients = models.ManyToManyField(User,
            related_name='recieved_pms',
            through='Recipient')
    created_at = models.DateTimeField(default=datetime.datetime.now)
    parent = models.ForeignKey('self',null=True,
        related_name ='parent_of')
    root_parent = models.ForeignKey('self',null=True,
        related_name ='root_parent_of')
    deleted = models.BooleanField(default=False)

    bbcode = BBCodeField('body')

    def __str__(self):
        return self.subject

    #there is clearly a one line query for this but this will
    #work for now
    def get_rec_str(self):
        """ return a string of all recipients usernames """

        rec_list = Recipient.objects.filter(message=self)
        rec_str =''
        for rec in rec_list:
            rec_str += rec.recipient.username + ' '
        return rec_str
    
    def get_reply_all(self, user):
        """ return a string of the users reply all will go to """

        reply_all = self.sender.username
        recips = Recipient.objects.filter(message=self).exclude(
            recipient=user).exclude(
            recipient=self.sender).select_related(
                'recipient__username')
        for recip in recips:
            reply_all = reply_all + ' ' + recip.recipient.username
        return reply_all

    def check_privacy(self, user):
        """returns true if user is a sender or recipient """
        if self.sender==user:
            return True
        if Recipient.objects.filter(message=self,recipient=user):
            return True
        return False

    def not_deleted(self, user):
        """returns true if there is a sender or recipient who hasn't deleted"""
        if self.sender == user:
            if self.deleted:
                return False
            else:
                return True
        if Recipient.objects.filter(message=self,
            recipient=user,deleted=False):
            return True
        return False

    
class Recipient(models.Model):
    """ a recipient of a pm
        recipient: the user
        message:  the PM
        read:    Have they read it yet
        deleted: have the deleted it
    """
    recipient = models.ForeignKey(User)
    message = models.ForeignKey(PM)
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.recipient.username


def clear_pm_count(sender, instance, signal, *args, **kwargs):
    """ when a new message is sent some users pm-count cache is cleared """
    cache_key = "pm-count:%d" %instance.recipient.id
    cache.delete(cache_key)
   
post_save.connect(clear_pm_count, sender=Recipient)
