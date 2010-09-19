from django.db import models
from django.contrib.auth.models import User

import datetime

class Invite(models.Model):
    inviter = models.ForeignKey(User,null=False)
    invitee = models.EmailField(null=False)
    created_on = models.DateTimeField(default=datetime.datetime.now)
    explanation = models.CharField(max_length=150, blank=True)
    approved = models.BooleanField(default=False)
    approved_on = models.DateTimeField(blank=True, null=True)
    invite_code = models.CharField(max_length=25,blank=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.invitee)
    
