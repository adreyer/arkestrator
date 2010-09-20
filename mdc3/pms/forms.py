from django import forms
from django.contrib.auth.models import User
from models import PM


class NewPMForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True)
    body = forms.TextField(required=False)
    recipients = forms.TextField(required=True)

    def clean_recipients():
        recipient_list = recipients.partion(' ')
        user_list = []
        for each rec in recipient_list:
            try:
                user_list.append(User.objects.get(username=rec))
            except User.DoesNotExist:
                raise forms.ValidationError(("User "+ rec +" not found"))
                                            
        self.cleaned_data[recep_list] = user_list
        return self.cleaned_data

    def save(user):
        pm = PM.objects.create(
            sender = user,
            subject = self.cleaned_data['subject']
            body = self.cleaned_data['body']
        )
        
        
        
        
