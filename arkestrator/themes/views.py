from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.base import RequestContext
from django.http import HttpResponseRedirect
from forms import ThemeForm
from models import Theme

@login_required
def edit_theme(request, theme_id=None):
    """ allows requester to edit their theme

        args:
        theme_id: The theme to fill the form with 

    """
    if not theme_id:
        try:
            theme = request.user.theme
        except Theme.DoesNotExist:
            theme = Theme(user = request.user)
    else:
        theme = get_object_or_404(Theme, pk=theme_id)

    if request.method == 'POST':
        if request.POST['submit'] == 'Save':
            form = ThemeForm(request.POST, instance=theme)
            if form.is_valid():
                form.save()
        else:
            # preview feature
            form = ThemeForm(request.POST, instance=theme)
            theme = form.save(commit=False)
    else:
        form = ThemeForm(instance=theme)

    return render_to_response("themes/edit_theme.html", { 
        'form' : form,
        'theme' : theme,
        'extra_themes' : Theme.objects.exclude(name="").all(),
    }, context_instance = RequestContext(request))
