from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext

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
