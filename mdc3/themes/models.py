from django.db import models
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context

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
    user = models.OneToOneField(User)

    background = models.CharField(max_length=6)
    row1 = models.CharField(max_length=6)
    row2 = models.CharField(max_length=6)
    form_background = models.CharField(max_length=6)
    my_posts = models.CharField(max_length=6)
    font_face = models.CharField(max_length=64)
    font_size = models.IntegerField(default=100)

    def text_color(self):
        return invert_color(self.background)

    def form_text_color(self):
        return invert_color(self.form_background)

    def render(self):
        template = get_template("themes/theme.css")
        return template.render(Context({'object': self}))
        
