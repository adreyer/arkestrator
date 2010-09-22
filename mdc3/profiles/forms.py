from django import forms
from django.contrib.auth.models import User
from models import Profile


class InfoUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email')

class InfoProfileForm(forms.ModelForm):
    model = Profile
    fields = ('name', 'location','email_publix',
              'aim_name','gtalk_name','website',
              'info','photo_url')

class PreferencesForm(forms.ModelForm):
    model = Profile
    field = ('show_images','collapse_size')
        
    
