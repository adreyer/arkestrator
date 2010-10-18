from django.contrib import admin

from models import Thread, Post, LastRead

class PostInline(admin.StackedInline):
    model = Post
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ('thread','body','created_at')
    
class ThreadAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['subject','creator','site','stuck']}),
    ]

class LastReadAdmin(admin.ModelAdmin):  
    list_display = ('user','thread','timestamp')

admin.site.register(Thread,ThreadAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(LastRead,LastReadAdmin)

