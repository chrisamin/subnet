"""
Module containing the URLconf for the subnet calculator. You can graft this
URLconf on to your URL tree using Django's include() helper.
"""
from django.conf.urls.defaults import *


urlpatterns = patterns('subnet.views',
    (r'^$', 'index'),
)
