from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context

import re
import colorsys

_COLOR_REGEX = re.compile("[0-9A-Fa-f]{6}")

def color_validator(self, value):
    if not _COLOR_REGEX.match(value):
        raise ValidationError("Color must have 6 hexadecimal characters")
    return value

class Theme(models.Model):
    user = models.OneToOneField(User)

    background = models.CharField(max_length=6)
    row1 = models.CharField(max_length=6)
    row2 = models.CharField(max_length=6)
    form_background = models.CharField(max_length=6)
    my_posts = models.CharField(max_length=6)
    font_face = models.CharField(max_length=64)
    font_size = models.IntegerField(default=100)

    clean_background = color_validator
    clean_row1 = color_validator
    clean_row2 = color_validator
    clean_form_background = color_validator
    clean_my_posts = color_validator

    def text_color(self):
        r = int(self.background[0:2], 16)
        g = int(self.background[2:4], 16)
        b = int(self.background[4:], 16)
        h,s,v = colorsys.rgb_to_hsv(r,g,b)
        if v > 127:
            return "000000"
        else:
            return "ffffff"

    def render(self):
        template = get_template("themes/theme.css")
        return template.render(Context({'object': self}))
        
