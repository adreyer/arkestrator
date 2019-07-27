import datetime
from django.contrib.auth.models import User
from django.db import models

class Ban(models.Model):
    """ creates a timed or permanant ban for a user """

    class Meta:
        permissions = (
                ('can_ban','Can ban users'),
                )
    user = models.ForeignKey(User,null=False,related_name='bans')
    creator = models.ForeignKey(User,null=False,related_name='created_bans')
    created_at = models.DateTimeField(default=datetime.datetime.now)
    reason = models.TextField(blank=False)
    start = models.DateTimeField(default=datetime.datetime.now)
    end = models.DateTimeField()
    permenant = models.BooleanField(default=False)
