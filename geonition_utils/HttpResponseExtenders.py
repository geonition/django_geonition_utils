from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.utils import simplejson as json

class HttpResponseCreated(HttpResponse):
    """
    TODO: should return location of resource created
    """
    def __init__(self, message):
        HttpResponse.__init__(self, message_to_json(message), status=201)
        
class HttpResponseUnauthorized(HttpResponse):
    """
    TODO: should return www-autenticate with OAuth (implement OAuth first)
    """
    def __init__(self, message):
        
        HttpResponse.__init__(self, message_to_json(message), status=401)
        #self['WWW-Authenticate'] = 'OAuth realm="%s"' % Site.objects.get_current().name

class HttpResponseConflict(HttpResponse):
    
    def __init__(self, message):
        HttpResponse.__init__(self, message_to_json(message), status=409)
        
class HttpResponseNotImplemented(HttpResponse):
    
    def __init__(self, message):
        HttpResponse.__init__(self, message_to_json(message), status=501)
        
        
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