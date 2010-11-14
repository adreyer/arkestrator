import pytz
from django import forms
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from mdc3.board.models import Thread, Post
from models import Event, RSVP, RSVP_CHOICES


class EditEventForm(forms.ModelForm):
    """ a form used to edit an existing event """
    time = forms.DateTimeField(required = True,
            label="Date and Time",
                        help_text="mm/dd/yy hh:mm (24 hour)")
    class Meta:
        model = Event
        fields = ('title','description','location','time','market')

    def clean(self):
        utc = pytz.timezone('UTC')
        ltz = pytz.timezone(self.cleaned_data['market'].timezone)
        local_time = ltz.localize(self.cleaned_data['time'])
        self.cleaned_data['time'] = local_time.astimezone(utc)
        return self.cleaned_data

    

class NewEventForm(forms.ModelForm):
    """ a form to create a new event """

    post = forms.CharField(required=True,
            label="Post:", widget=forms.TextInput(attrs={'size': 70}))
    time = forms.DateTimeField(required = True,
            label="Date and Time",
            help_text="mm/dd/yy hh:mm (24 hour)")
    class Meta:
        model  = Event
        fields = ('title','description','location','time',
                  'market','post')

    def save(self, user):
        utc = pytz.timezone('UTC')
        ltz = pytz.timezone(self.cleaned_data['market'].timezone)
        local_time = ltz.localize(self.cleaned_data['time'])
        time = local_time.astimezone(utc)
        thread = Thread(
            creator =   user,
            subject =   self.cleaned_data['title'],
            site    =   Site.objects.get_current(),
            )
        thread.save()
        post = Post(
            thread  =   thread,
            creator =   user,
            body    =   self.cleaned_data['post']
            )
        post.save()
        thread.last_post = post
        thread.save()
        event = Event(
            thread      =   thread,
            creator     =   user,
            title       =   self.cleaned_data['title'],
            description =   self.cleaned_data['description'],
            location    =   self.cleaned_data['location'],
            time        =   time,
            market      =   self.cleaned_data['market']
            )
        event.save()
        return event


class RSVPForm(forms.Form):
    """ a form to create or modify an rsvp """
    attend = forms.ChoiceField(RSVP_CHOICES, label="Will you Attend?")
        
    def save(self, user, event):
        try:
            rsvp = RSVP.objects.get(event=event,user=user) 
            if rsvp.attending != self.cleaned_data['attend']:
                rsvp.attending = self.cleaned_data['attend']
                rsvp.save()
        except RSVP.DoesNotExist:
            rsvp = RSVP(event=event, user=user,
                    attending=self.cleaned_data['attend'])
            rsvp.save()
        return rsvp
    
