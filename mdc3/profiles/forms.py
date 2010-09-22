from django import forms
from django.contrib.auth.models import User
from models import Profile


class InfoUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email')

class InfoProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'location', 'phone', 'email_public',
                  'aim_name', 'gtalk_name', 'website',
                  'info', 'photo_url')

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Profile
        field = ('show_images','collapse_size')
        
    
