from django.http import HttpResponse
from django.contrib.sites.models import Site

class HttpResponseCreated(HttpResponse):
    
    def __init__(self, message):
        HttpResponse.__init__(self, message, status=201)
        
class HttpResponseUnauthorized(HttpResponse):

    def __init__(self, message):
        HttpResponse.__init__(self, message, status=401)
        #self['WWW-Authenticate'] = 'OAuth realm="%s"' % Site.objects.get_current().name

class HttpResponseConflict(HttpResponse):
    
    def __init__(self, message):
        HttpResponse.__init__(self, message, status=409)
        
class HttpResponseNotImplemented(HttpResponse):
    
    def __init__(self, message):
        HttpResponse.__init__(self, message, status=501)