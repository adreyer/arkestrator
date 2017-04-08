from django import forms
from django.contrib.auth.models import User
from arkestrator.invites.models import Invite
from arkestrator.profiles.models import Profile

import datetime
import re

class NewInviteForm(forms.Form):
    """ a form to create a new invite """
    invitee = forms.EmailField(required=True, label="Email", widget=forms.TextInput(attrs={'size': 70, 'maxlength': 160}))
    explanation = forms.CharField(max_length=2500,
        label="Explain",
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 70}))

    def save(self, user):
        invite = Invite.objects.create(
            inviter = user,
            invitee = self.cleaned_data['invitee'],
            explanation = self.cleaned_data['explanation']
            )
        return invite

class UserRegistrationForm(forms.ModelForm):
    """ a form to register a new user """
    username = forms.CharField(max_length = 20,
            help_text = 'Required. 20 characters or fewer. Letters, numbers and @/./+/-/_ characters')
    class Meta:
        model = User
        fields = ('username', 'email')
    pass1 = forms.CharField(required=True,
            label="Password",
            widget=forms.PasswordInput)
    pass2 = forms.CharField(required=True,
            label="Password (confirm)",
            widget=forms.PasswordInput)

    #don't allow whitespace in usernames
    def clean_username(self):
        """ make sure there is no whitespace in usernames """
        username = self.cleaned_data['username']
        if re.search(r'[^a-zA-Z0-9@.+-_]', username):
            raise forms.ValidationError(
                    "Only letters, numbers and @/./+/-/_ characters are allowed in usernames.  No whitespace")
        # Not sure why this isn't happening automatically
        if User.objects.filter(username=username):
            raise forms.ValidationError("Sorry that username is already in use")
        return self.cleaned_data['username']

    def clean(self):
        """ verify that both passwords match """
        if self.cleaned_data["pass1"] != self.cleaned_data["pass2"]:
            raise forms.ValidationError("Passwords don't match.")
        return self.cleaned_data

class ProfileRegistrationForm(forms.ModelForm):
    """ the profile part of registration """
    class Meta:
        model = Profile
        fields = ('name', 'location')

        


    
