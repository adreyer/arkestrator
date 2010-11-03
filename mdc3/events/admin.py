from django.contrib import admin
from models import Market, Event, RSVP

class EventAdmin(admin.ModelAdmin):
    list_display=('title','time','description','market',
        'creator','created_at','all_markets')

class RSVPAdmin(admin.ModelAdmin):
    list_display=('event','user','attending')

admin.site.register(Market)
admin.site.register(Event,EventAdmin)
admin.site.register(RSVP, RSVPAdmin)
