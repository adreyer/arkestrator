import json
import urllib
import base64

from django.contrib.auth.models import User
from django import forms

from arkestrator.gallery.models import Image
from arkestrator.gallery.key_file import key

class IMGForm(forms.Form):
    img_file=forms.FileField(label='image')
    title=forms.CharField(max_length=160)
    description=forms.CharField(max_length=1000,
        widget=forms.Textarea(attrs={'cols': 70, 'rows': 12, 'class': 'legend'}))

    def validate_img_file(self):
        if self.cleaned_data['img_file'].size > 10000000:
            raise forms.ValidationError("image larger than 10MB")
        return self.cleaned_data['img_file']

    def save(self, user):
        image = self.cleaned_data['img_file'].read()
        data = urllib.urlencode({
                    'key': key,
                    'image' : base64.b64encode(image)})
        response = urllib.urlopen('http://imgur.com/api/upload.json',data)
        rsp = json.loads(response.read())['rsp']
        print rsp
        if rsp['stat'] == 'fail':
            raise forms.ValidationError('imgur error:' + rsp['error_msg'])
        image = Image(
            uploader    =   user,
            title       =   self.cleaned_data['title'],
            description =   self.cleaned_data['description'],
            url         =   rsp['image']['original_image'],
            image_hash  =   rsp['image']['image_hash'],
            delete_hash =   rsp['image']['delete_hash'],
            )
        image.save()
        return image


