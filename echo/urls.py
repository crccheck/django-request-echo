from collections import OrderedDict
from copy import copy
from operator import concat
import json
import random
import string

from django.conf.urls import patterns, url
from django.http import HttpResponse
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
    def get_fake_word(self):
        n = random.randint(3, 12)
        return reduce(concat, [random.choice(string.ascii_letters) for __ in range(n)])

    def get_fake_link(self):
        n = random.randint(1, 5)
        out = '/' + '/'.join([self.get_fake_word() for __ in range(n)])
        if random.randint(0, 3):
            # sometimes give a trailing slash
            out += '/'
        return out


    def get(self, request, *args, **kwargs):
        # filter META down to just the standard stuff
        request_data = copy(request)
        meta = [(x, y) for x, y in request_data.META.items() if
            x in META or x.startswith('HTTP_')]
        request_data.META = OrderedDict(sorted(meta))
        context = {
            'next': self.get_fake_link(),
            'request': request_data,
        }

        # TODO check 'Accept' header
        return_json = request.is_ajax()
        if return_json:
            # recreation of wow.html
            data = dict(
                body=request_data.body,
                path=request_data.path_info,
                full_path=request_data.get_full_path(),
                method=request_data.method,
                encoding=request.encoding,
                META=request_data.META,
                GET=request_data.GET,
                POST=request_data.POST,
                COOKIES=request_data.COOKIES,
            )
            response = HttpResponse(json.dumps(data),
                    content_type='application/json')
        else:
            response = render_to_response('wow.html', context)
        # Do not use X headers
        # http://tools.ietf.org/html/draft-ietf-appsawg-xdash-05
        # http://en.wikipedia.org/wiki/List_of_HTTP_header_fields#Responses
        response['Readme'] = 'https://github.com/crccheck/django-request-echo'
        # https://developers.google.com/webmasters/control-crawl-index/docs/robots_meta_tag
        response['X-Robots-Tag'] = 'noindex'
        return response

    post = get  # TEEHEE


urlpatterns = patterns('',
    url(r'', Wow.as_view()),
)
