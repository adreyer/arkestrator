from django import forms
from django.contrib.auth.models import User
from models import PM, Recipient


class NewPMForm(forms.Form):
    recipients = forms.CharField(required=True,
            label="To:(Enter usernames seperated by spaces)")
    subject = forms.CharField(max_length=100, required=True)
    body = forms.CharField(required=False,
            widget=forms.Textarea)
    

    def clean_recipients(self):
        recipient_list = self.cleaned_data['recipients'].split()
        user_list = []
        for rec in recipient_list:
            try:
                user_list.append(User.objects.get(username=rec))
            except User.DoesNotExist:
                raise forms.ValidationError(("User "+ rec +" not found"))
                                            
        self.cleaned_data['recipients_user'] = set(user_list)
        return self.cleaned_data

    def save(self, user):
        pm = PM(
            sender = user,
            subject = self.cleaned_data['subject'],
            body = self.cleaned_data['body']
        )
        pm.save()

        for user in self.cleaned_data['recipients_user']:
            recip = Recipient(recipient=user, message=pm)
            recip.save()
        
        
        
        
