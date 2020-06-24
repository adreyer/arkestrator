from django.contrib import admin
from .models import Invite

class InviteAdmin(admin.ModelAdmin):
    list_display = ('invitee', 'inviter', 'created_on',
                    'approved', 'rejected','used')

admin.site.register(Invite, InviteAdmin)
