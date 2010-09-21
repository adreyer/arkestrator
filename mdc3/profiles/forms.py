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
        


            
##from mdc3.profiles.models import Profile
##
##class PrefForm(forms.Form):
##    email_public = forms.BooleanField()
##    show_images = forms.BooleanField()
##    def save(self, profile, user):
##        profile.email_public =  self.cleaned_data['email_public'],
##        profile.show_images = self.cleaned_data['show_images'],
##        #since we didn't create a profile only modified one do we have
##        #return it to save it?
##        #return profile
##
##
##class InfoForm(forms.Form):
##    name = forms.CharField(max_length=60)
##    email = forms.EmailField(max_length=60)
##
##    def save(self, user):
##        user.first_name = self.name
##        user.email = self.email
##        user.save()

##    zip_code = forms.CharField(max_length=25)
##    city = models.CharField(max_lenth=50)
##    location = models.CharField(max_lenth=50)
##    aim_name = models.CharField(max_lenth=50)
##    gchat_name = models.CharField(max_lenth=50)
##    website = models.URLField(max_lenth=150)
##    info = models.CharField(widget=forms.Textarea, max_lenth=2500)
    
