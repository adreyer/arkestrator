from django import forms
from django.contrib.auth.models import User
from mdc3.invites.models import Invite
from mdc3.profiles.models import Profile

import datetime
import re

class NewInviteForm(forms.Form):
    invitee = forms.EmailField(required=True, label="Email of Invitee")
    invitee2 = forms.EmailField(required=True, label="Email(verify)")
    explanation = forms.CharField(max_length=150,
        label="Who the fuck is this person",
        widget=forms.Textarea)

    def clean(self):
        if self.cleaned_data["invitee"] != self.cleaned_data["invitee2"]:
            raise forms.ValidationError("emails don't match")
        return self.cleaned_data

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

    #don't allow whitespace in usernames
    def clean_username(self):
        if re.search(r'\s', self.cleaned_data['username']):
            raise forms.ValidationError(
                    "no whitespace if usernames, perhaps you'd like to use an _")
        return self.cleaned_data['username']

    def clean(self):
        if self.cleaned_data["pass1"] != self.cleaned_data["pass2"]:
            raise forms.ValidationError("passwords don't match")
        return self.cleaned_data
        
        
            
            
        

class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'location')

        


    
