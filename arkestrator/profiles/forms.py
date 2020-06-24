from django import forms
from django.contrib.auth.models import User
from arkestrator.events.models import Market
from .models import Profile




class InfoProfileForm(forms.ModelForm):
    """ change the publicly viewable info """
    email_public = forms.CharField(label='Public email', widget=forms.TextInput(attrs={'size': 70, 'maxlength': 160}), required=False)
    aim_name = forms.CharField(label='AIM', widget=forms.TextInput(attrs={'size': 70, 'maxlength': 160}), required=False)
    gtalk_name = forms.CharField(label='Jabber', widget=forms.TextInput(attrs={'size': 70, 'maxlength': 160}), required=False)
    photo_url = forms.CharField(label='Picture URL', widget=forms.TextInput(attrs={'size': 70, 'maxlength': 160}), required=False)
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
    """ change the private preferences """
    collapse_size = forms.IntegerField(label='Previously seen posts redisplayed')
    favs_first = forms.BooleanField(
                    label='Unread favorite threads displayed first', 
                    required=False)
    market = forms.ModelChoiceField(queryset=Market.objects.all(),
                label='Which city do you want to see events for',
                empty_label='All Cities',
                required = False)
    class Meta:
        model = Profile
        fields = ('show_images','collapse_size','favs_first',
                  'market', 'time_zone')

class PrivEmailForm(forms.ModelForm):
    """ change the private email associated with a user """
    email = forms.CharField(label='Private email', widget=forms.TextInput(attrs={'size': 70, 'maxlength': 160}), required=False)
    class Meta:
        model = User
        fields = ('email',)
