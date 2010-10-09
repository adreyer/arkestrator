from django import forms
from django.contrib.auth.models import User
from models import Profile


class InfoUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email')

class InfoProfileForm(forms.ModelForm):
    email_public = forms.CharField(label='Public email', widget=forms.TextInput(attrs={'size': 70, 'maxlength': 160}))
    aim_name = forms.CharField(label='AIM', widget=forms.TextInput(attrs={'size': 70, 'maxlength': 160}))
    gtalk_name = forms.CharField(label='Jabber', widget=forms.TextInput(attrs={'size': 70, 'maxlength': 160}))
    photo_url = forms.CharField(label='Picture URL', widget=forms.TextInput(attrs={'size': 70, 'maxlength': 160}))
    class Meta:
        model = Profile
        fields = ('name', 'location', 'phone', 'email_public',
                  'aim_name', 'gtalk_name', 'website',
                  'info', 'photo_url')
        widgets = {
            'name': forms.TextInput(attrs={'size': 70, 'maxlength': 160}),
            'location': forms.TextInput(attrs={'size': 70, 'maxlength': 160}),
            'phone': forms.TextInput(attrs={'size': 70, 'maxlength': 160}),
            'gtalk_name': forms.TextInput(attrs={'size': 70, 'maxlength': 160}),
            'website': forms.TextInput(attrs={'size': 70, 'maxlength': 160}),
            'info': forms.Textarea(attrs={'cols': 70, 'rows': 12, 'class': 'legend'}),
        }

class PrefsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('show_images','collapse_size')
