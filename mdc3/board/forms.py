from django import forms
from mdc3.board.models import Thread, Post
from django.contrib.sites.models import Site

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ('subject',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

