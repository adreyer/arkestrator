from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from forms import ThemeForm
from models import Theme

@login_required
def edit_theme(request):
    try:
        theme = request.user.theme
    except Theme.DoesNotExist:
        theme = Theme(user = request.user)

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
    }, context_instance = RequestContext(request))
