from collections import OrderedDict
from copy import copy

from django.conf.urls import patterns, url
from django.shortcuts import render_to_response
from django.views.generic import View


# additional META to display besides HTTP_*
META = (
    'CONTENT_LENGTH',
    'CONTENT_TYPE',
    'QUERY_STRING',
    'REMOTE_ADDR',
    'REMOTE_HOST',
    'REQUEST_METHOD',
    'SERVER_NAME',
    'SERVER_PORT',
)


class Wow(View):
    """such view."""
    def get(self, request, *args, **kwargs):
        # filter META down to just the standard stuff
        request_data = copy(request)
        meta = [(x, y) for x, y in request_data.META.items() if
            x in META or x.startswith('HTTP_')]
        request_data.META = OrderedDict(sorted(meta))
        context = {'request': request_data}
        return render_to_response('wow.html', context)

    post = get  # TEEHEE


urlpatterns = patterns('',
    url(r'', Wow.as_view()),
)
