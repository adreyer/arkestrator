import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from arkestrator.board.models import Thread

class Market(models.Model):
    """   A city or region in which events take place

         Attrs:
         name:  What the market will be called
         timezone: what timezone the market is in
   """

    name=models.CharField(max_length=20)
    timezone=models.CharField(max_length=50,
                        default=settings.DEFAULT_TZ,
                        choices=settings.TZ_CHOICES,)

    def __str__(self):
        return self.name

class Event(models.Model):
    """   An event

        attrs:
        thread: the thread associated with this event
        creator:  who created this event
        description: what is this event
        time:        a UTC datetime of when the event takes place
        location:   where is the event
        market:     what market is it in
        all_markets: should the event be displayed for all users regardless 
            of what market they have selected
        created_at:  UTC datetime when the event was created
        rsvps:      the rsvps for the event
    """

    class Meta:
        permissions=(('can_edit', 'Can Edit Events'),)

    thread = models.OneToOneField(Thread,null=False)
    creator = models.ForeignKey(User,null=False)
    description = models.TextField(blank=True)
    time = models.DateTimeField(null=False)
    location = models.TextField(null=True)
    market = models.ForeignKey(Market,null=False)
    all_markets = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    rsvps = models.ManyToManyField(User, through='RSVP',
                related_name='rsvps')

    #this should be cached
    def rsvp_list(self):
        """ return rsvps for an event
            I don't remember why this is here(amd)
        """
        return RSVP.objects.filter(event=self).order_by('user__username')

    def __str__(self):
        return self.thread.subject

RSVP_CHOICES = (
        ( 'Yes' , 'Yes'),
        ( 'Maybe' , 'Maybe'),
        ( 'No' , 'No'),
        )

class RSVP(models.Model):
    """ an rsvp
        attrs:
        event: what event is it for
        user:  whose rsvp is it
        attending: what is there attending status
    """

    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    attending = models.CharField(max_length=5, choices=RSVP_CHOICES,
                default='Yes')
    



