from django.contrib import admin

from models import Thread, Post

class PostInline(admin.StackedInline):
    model = Post
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ('thread','body','created_at')
    
class ThreadAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['subject','creator','site','stuck']}),
    ]


admin.site.register(Thread,ThreadAdmin)
admin.site.register(Post,PostAdmin)

