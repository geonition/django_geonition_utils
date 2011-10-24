from django.http import HttpResponse as DjangoHttpResponse
from django.http import HttpResponseBadRequest as DjangoHttpResponseBadRequest
from django.http import HttpResponseForbidden as DjangoHttpResponseForbidden
from django.http import HttpResponseNotFound as DjangoHttpResponseNotFound
from django.contrib.sites.models import Site
from django.utils import simplejson as json

#200
class HttpResponse(DjangoHttpResponse):
    
    def __init__(self, message):
        DjangoHttpResponse.__init__(self,
                                    message_to_json(message),
                                    status=200,
                                    content_type='application/json')

#201
class HttpResponseCreated(DjangoHttpResponse):
    """
    TODO: should return location of resource created
    """
    def __init__(self, message):
        DjangoHttpResponse.__init__(self,
                                    message_to_json(message),
                                    status=201,
                                    content_type='application/json')


#400
class HttpResponseBadRequest(DjangoHttpResponseBadRequest):
    
    def __init__(self, message):
        DjangoHttpResponseBadRequest.__init__(self,
                                              message_to_json(message),
                                              content_type='application/json')

#403    
class HttpResponseForbidden(DjangoHttpResponseForbidden):
    
    def __init__(self, message):
        DjangoHttpResponseForbidden.__init__(self,
                                             message_to_json(message),
                                             content_type='application/json')

#404
class HttpResponseNotFound(DjangoHttpResponse):
    
    def __init__(self, message):
        DjangoHttpResponse.__init__(self,
                                    message_to_json(message),
                                    status=404,
                                    content_type='application/json')

        
class HttpResponseUnauthorized(DjangoHttpResponse):
    """
    TODO: should return www-autenticate with OAuth (implement OAuth first)
    """
    def __init__(self, message):
        
        DjangoHttpResponse.__init__(self,
                                    message_to_json(message),
                                    status=401,
                                    content_type='application/json')
        #self['WWW-Authenticate'] = 'OAuth realm="%s"' % Site.objects.get_current().name

class HttpResponseConflict(DjangoHttpResponse):
    
    def __init__(self, message):
        DjangoHttpResponse.__init__(self,
                                    message_to_json(message),
                                    status=409,
                                    content_type='application/json')
        
class HttpResponseNotImplemented(DjangoHttpResponse):
    
    def __init__(self, message):
        DjangoHttpResponse.__init__(self,
                                    message_to_json(message),
                                    status=501,
                                    content_type='application/json')
        
        
def message_to_json(message):
    """
    This function turnes the string message to a json
    string, this is to make all REST responses
    to be in JSON format and easier to implement
    in a consistent way.
    """
    
    #if message is alreay in json then do not do anything
    mesage_dict = {}
    
    try:
        message_dict = json.loads(message)
    except ValueError:
        message_dict = {
            "msg": message
        }
        
    return json.dumps(message_dict)