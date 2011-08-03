import re

from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers

from django import http

import settings
XS_SHARING_ALLOWED_ORIGINS = getattr(settings, "XS_SHARING_ALLOWED_ORIGINS", [])
XS_SHARING_ALLOWED_METHODS = getattr(settings, "XS_SHARING_ALLOWED_METHODS", [])
XS_SHARING_ALLOWED_HEADERS = getattr(settings, "XS_SHARING_ALLOWED_HEADERS", [])


class CrossSiteAccessMiddleware(object):


    def process_request(self, request):

        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin'] = ",".join( XS_SHARING_ALLOWED_ORIGINS )
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
            response['Access-Control-Allow-Headers'] = ",".join( XS_SHARING_ALLOWED_HEADERS )
            
            return response

        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response

        response['Access-Control-Allow-Origin'] = ",".join( XS_SHARING_ALLOWED_ORIGINS )
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
        response['Access-Control-Allow-Headers'] = ",".join( XS_SHARING_ALLOWED_HEADERS )

        return response
    
class PreventCacheMiddleware(object):

    def process_response(self, request, response):

        response['Pragma'] = 'no-cache'
        response['Cache-Control'] = 'max-age=0,no-cache,no-store,post-check=0,pre-check=0'
        response['Expires'] = '0'

        return response
