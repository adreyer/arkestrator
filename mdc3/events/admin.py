from django.contrib import admin
from models import Market, Event

class EventAdmin(admin.ModelAdmin):
    list_display=('title','time','description','creator')

admin.site.register(Market)
admin.site.register(Event,EventAdmin)
