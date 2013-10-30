import re

from django.conf import settings
from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers
from http import HttpResponseBadRequest
from http import HttpResponse

XS_SHARING_ALLOWED_ORIGINS = getattr(settings, "XS_SHARING_ALLOWED_ORIGINS", [])
XS_SHARING_ALLOWED_METHODS = getattr(settings, "XS_SHARING_ALLOWED_METHODS", [])
XS_SHARING_ALLOWED_HEADERS = getattr(settings, "XS_SHARING_ALLOWED_HEADERS", [])


class CrossSiteAccessMiddleware(object):


    def process_request(self, request):

        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = HttpResponse()
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
        if response.has_header('gnt-force-cache-control'):
            del response['gnt-force-cache-control']
            return response
        else:
            response['Pragma'] = 'no-cache'
            response['Cache-Control'] = 'max-age=0,no-cache,no-store,post-check=0,pre-check=0'
            response['Expires'] = '0'

            return response

class RESTExceptionMiddleware(object):
    """
    This middleware handles exception thrown by the
    REST interface. The Exceptions are transformed to
    JSON responses with an appropriate http code.
    
    This middleware should only be used with REST where
    you do not want requests to get 500 error messages but
    some more usefull error messages.
    """
    def process_exception(self, request, exception):
        return HttpResponseBadRequest(exception.message)
        

class IEEdgeMiddleware(object):
    """
    This middleware sets header for IE to address the issue
    of the html meta tag not always working for the case of:
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    """
    def process_response(self, request, response):
        
        if 'MSIE' in  request.META.get('HTTP_USER_AGENT',''):
            response['X-UA-Compatible'] = "IE=Edge,chrome=1"
        
        return response

