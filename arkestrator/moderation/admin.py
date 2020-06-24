from django.contrib import admin

from .models import Ban

class BanAdmin(admin.ModelAdmin):
    list_display = ('user','reason','start','end')

admin.site.register(Ban,BanAdmin)
