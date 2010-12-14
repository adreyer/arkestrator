
from django import forms
from models import Ban

class BanForm(forms.ModelForm):
    class Meta:
        model = Ban
        fields = ('user','reason','start','end')
