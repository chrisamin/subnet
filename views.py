from __future__ import absolute_import

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from . import forms


def index(request, template_name="subnet/index.html"):
    """
    The index view for the subnet calculator.
    """
    if request.method == "POST":
        data = request.POST
    else:
        data = {
            "address": request.META.get("REMOTE_ADDR", "127.0.0.1"),
            "cidr": 0,
        }

    form = forms.SubnetForm(data)

    context = {
        "form": form,
        }
    return render_to_response(template_name, context,
        context_instance=RequestContext(request))


def json(request):
    """
    Function acting as a JSON version of the index view.
    """
    form = forms.SubnetForm(request.GET)
    if not form.is_valid():
        return HttpResponse(simplejson.dumps(form.errors))
    output = simplejson.dumps(form.cleaned_data)
    return HttpResponse(output)
