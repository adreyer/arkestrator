from django.contrib import admin
from models import PM, Recipient

class PMAdmin(admin.ModelAdmin):
    pass

admin.site.register(PM, PMAdmin)
