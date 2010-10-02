from django.db import models
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context
from django.core.urlresolvers import reverse

import colorsys

def invert_color(color):
    r = int(color[:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:], 16)
    h,s,v = colorsys.rgb_to_hsv(r,g,b)
    if v > 127:
        return "000000"
    else:
        return "ffffff"

class Theme(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True)

    background = models.CharField(max_length=6, default="eeeeee")
    row1 = models.CharField(max_length=6, default="e0e4e8")
    row2 = models.CharField(max_length=6, default="d0d4d8")
    form_background = models.CharField(max_length=6, default="ffffff")
    my_posts = models.CharField(max_length=6, default="e8e4e0")
    font_face = models.CharField(max_length=64, default="sans-serif")
    font_size = models.IntegerField(default=95)

    def text_color(self):
        return invert_color(self.background)

    def form_text_color(self):
        return invert_color(self.form_background)

    def render(self):
        template = get_template("themes/theme.css")
        return template.render(Context({'object': self}))

    def get_absolute_url(self):
        return reverse('theme-css', args=(self.id,))

