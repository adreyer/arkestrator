from django.contrib import admin
from models import PM, Recipient

class PMAdmin(admin.ModelAdmin):
    pass

class RecipientAdmin(admin.ModelAdmin):
    pass

admin.site.register(PM, PMAdmin)
admin.site.register(Recipient, RecipientAdmin)
