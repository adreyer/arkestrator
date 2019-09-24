from django import forms
from django.core.exceptions import ValidationError
import re

from .models import Theme

_COLOR_REGEX = re.compile("[0-9A-Fa-f]{6}")

def color_cleaner(name):
    """ true if name is a valid 6 hex color  """
    def _color_cleaner(self):
        if not _COLOR_REGEX.match(self.cleaned_data[name]):
            raise ValidationError("Color must have 6 hexadecimal characters")
        return self.cleaned_data[name]
    return _color_cleaner

class ThemeForm(forms.ModelForm):
    """ a form to change a theme """
    class Meta:
        model = Theme
        exclude = ('user','name')

    clean_background = color_cleaner('background')
    clean_row1 = color_cleaner('row1')
    clean_row2 = color_cleaner('row2')
    clean_form_background = color_cleaner('form_background')
    clean_my_posts = color_cleaner('my_posts')

