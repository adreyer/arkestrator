from django.db import models
from django.contrib.auth.models import User

import datetime

class Invite(models.Model):
    """ an invite

        inviter: user who created the invite
        invitee: email of the person to send the invite too
        created_on: when the invite was created
        explanation: why this person is being invited
        approved: is this invite approved by a mod
        approved by:  which mod last approved or rejected this invite
        approved on:  when was the last approval/rejection made
        invite_code:  the code to use the invite
        used:  has this invite been used 

    """

    class Meta:
        permissions = (
            ("can_approve","Can approve invites"),
        )
        
    inviter = models.ForeignKey(User,null=False,
            related_name='created_invite')
    invitee = models.EmailField(null=False)
    created_on = models.DateTimeField(default=datetime.datetime.now)
    explanation = models.CharField(max_length=150, blank=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User,null=True,
            related_name='approved_invite')
    approved_on = models.DateTimeField(blank=True, null=True)
    invite_code = models.CharField(max_length=25,blank=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.invitee)
    
