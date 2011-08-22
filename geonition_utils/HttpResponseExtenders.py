from django.http import HttpResponse
from django.contrib.sites.models import Site

class HttpResponseCreated(HttpResponse):
    """
    TODO: should return location of resource created
    """
    def __init__(self, message):
        HttpResponse.__init__(self, message, status=201)
        
class HttpResponseUnauthorized(HttpResponse):
    """
    TODO: should return www-autenticate with OAuth (implement OAuth first)
    """
    def __init__(self, message):
        HttpResponse.__init__(self, message, status=401)
        #self['WWW-Authenticate'] = 'OAuth realm="%s"' % Site.objects.get_current().name

class HttpResponseConflict(HttpResponse):
    
    def __init__(self, message):
        HttpResponse.__init__(self, message, status=409)
        
class HttpResponseNotImplemented(HttpResponse):
    
    def __init__(self, message):
        HttpResponse.__init__(self, message, status=501)