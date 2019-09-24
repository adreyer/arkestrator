from django.db import models
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.core.urlresolvers import reverse

import colorsys
import time

def invert_color(color):
    """ return black or white to display on top of color """
    r = int(color[:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:], 16)
    h,s,v = colorsys.rgb_to_hsv(r,g,b)
    if v >= 156:
        return "000000"
    else:
        return "ffffff"

class Theme(models.Model):
    """ A theme """
    user = models.OneToOneField(User, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True)

    background = models.CharField(max_length=6, default="eeeeee")
    row1 = models.CharField(max_length=6, default="dae1e8")
    row2 = models.CharField(max_length=6, default="c9d0d8")
    form_background = models.CharField(max_length=6, default="ffffff")
    my_posts = models.CharField(max_length=6, default="e8e1da")
    font_face = models.CharField(max_length=64, default="sans-serif")
    font_size = models.IntegerField(default=95)

    updated = models.DateTimeField(auto_now=True)

    def background_text_color(self):
        return invert_color(self.background)

    def row1_text_color(self):
        return invert_color(self.row1)

    def row2_text_color(self):
        return invert_color(self.row2)

    def mypost_text_color(self):
        return invert_color(self.my_posts)

    def form_text_color(self):
        return invert_color(self.form_background)

    def render(self):
        template = get_template("themes/theme.css")
        return template.render({'object': self})

    def get_absolute_url(self):
        return "%s?ts=%d" % (reverse('theme-css', args=(self.id,)),
            int(time.mktime(self.updated.timetuple())))

