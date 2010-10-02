from django import forms
from django.contrib.auth.models import User
from mdc3.invites.models import Invite
from mdc3.profiles.models import Profile

import datetime

class NewInviteForm(forms.Form):
    invitee = forms.EmailField(required=True, label="Invitees's email adress")
    explanation = forms.CharField(max_length=150,
        label="Who the fuck is this person",
        widget=forms.Textarea)

    def save(self, user):
        invite = Invite.objects.create(
            inviter = user,
            invitee = self.cleaned_data['invitee'],
            explanation = self.cleaned_data['explanation']
            )
        return invite

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')
    
    pass1 = forms.CharField(required=True,
            label="password",
            widget=forms.PasswordInput)
    pass2 = forms.CharField(required=True,
            label="retype password",
            widget=forms.PasswordInput)

    def clean(self):
        if self.cleaned_data["pass1"] != self.cleaned_data["pass2"]:
            raise forms.ValidationError("passwords don't match")
        return self.cleaned_data
        
        
            
            
        

class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'location')

        


    
