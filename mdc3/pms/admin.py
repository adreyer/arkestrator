from django.contrib import admin
from models import PM, Recipient

class PMAdmin(admin.ModelAdmin):
    list_display = ('sender', 'subject', 'created_on', 'parent')

class RecipientAdmin(admin.ModelAdmin):
    list_display = ('message','recipient','read')

admin.site.register(PM, PMAdmin)
admin.site.register(Recipient, RecipientAdmin)
