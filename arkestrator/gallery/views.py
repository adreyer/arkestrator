from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.db.models.signals import post_save
from django.db.models import Sum, Count, Max, F
from django.core.cache import cache
from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth.models import User

import forms
from models import Image

@login_required
def upload_image(request):
    if request.method == 'POST':
        print request
        print request.FILES
        print request.FILES['img_file']
        form = forms.IMGForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(request.user)
            return HttpResponseRedirect(reverse(
                'view-image', args=[image.id]))
    else:
        form = forms.IMGForm()
    return render_to_response('gallery/upload_image.html',
            { 'form' : form },
            context_instance = RequestContext(request))

@login_required
def view_image(request, id):
    image = get_object_or_404(Image, pk=id)
    return render_to_response('gallery/view_image.html',
            { 'image' : image },
            context_instance = RequestContext(request))
