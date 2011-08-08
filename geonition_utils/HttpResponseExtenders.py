from django.http import HttpResponse
from django.contrib.sites.models import Site

class HttpResponseNotAuthorized(HttpResponse):

    def __init__(self, message):
        HttpResponse.__init__(self, message, status=401)
        #self['WWW-Authenticate'] = 'Basic realm="%s"' % Site.objects.get_current().name


class HttpResponseNotImplemented(HttpResponse):
    
    def __init__(self, message):
        HttpResponse.__init__(self, message, status=501)