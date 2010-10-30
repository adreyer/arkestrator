import datetime
from django.db import models
from django.contrib.auth.models import User

class Market(models.Model):
    name=models.CharField(max_length=20)
    timezone=models.CharField(max_length=50,
                        default='US/Eastern')

    def __str__(self):
        return self.name
    
class Event(models.Model):
    class Meta:
        permissions=(('can_edit', 'Can Edit Events'),)
    
    from mdc3.board.models import Thread
    thread = models.OneToOneField(Thread,null=False)
    creator = models.ForeignKey(User,null=False)
    title = models.CharField(max_length=160,blank=False)
    description = models.TextField(blank=True)
    time = models.DateTimeField(null=False)
    location = models.TextField(null=True)
    market = models.ForeignKey(Market,null=False)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    rsvps = models.ManyToManyField(User, through='RSVP',
                related_name='rsvps')


    def __str__(self):
        return self.title

class RSVP(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    status = models.IntegerField()
    



