from django.contrib import admin
from models import Invite

class InviteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Invite, InviteAdmin)
