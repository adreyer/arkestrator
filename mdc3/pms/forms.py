from django import forms
from django.contrib.auth.models import User
from models import PM, Recipient
import bbcode


class NewPMForm(forms.ModelForm):
    recs = forms.CharField(required=True,
            label="To:", widget=forms.TextInput(attrs={'size': 60}))
    
    class Meta:
        model = PM
        fields = ('recs','subject', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'cols': 60, 'rows': 12}),
            'subject': forms.TextInput(attrs={'size': 60, 'maxlength': 160})
        }
        
    def clean_recs(self):
        recipient_list = self.cleaned_data['recs'].split()
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
        return pm
        
        
        
        
