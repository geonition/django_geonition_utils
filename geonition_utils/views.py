"""
This file contains view classes that can be used in other applications.
"""
from geonition_utils.HttpResponseExtenders import HttpResponseNotImplemented
from django.views.generic import View

class RequestHandler(View):
    """
    This class should be inherited by the view
    classes to be used for implementing REST
    """
    def __init__(self):
        pass
    
    def get(self, request, *args, **kwargs):
        """
        This method should be overridden
        """
        return HttpResponseNotImplemented("not implemented, yet!")
    
    def post(self, request, *args, **kwargs):
        """
        This method should be overridden
        """
        return HttpResponseNotImplemented("not implemented, yet!")
    
    def put(self, request, *args, **kwargs):
        """
        This method should be overridden
        """
        return HttpResponseNotImplemented("not implemented, yet!")
    
    def delete(self, request, *args, **kwargs):
        """
        This method should be overridden
        """
        return HttpResponseNotImplemented("not implemented, yet!")
        
    def options(self, request, *args, **kwargs):
        """
        This method should be overridden
        """
        return HttpResponseNotImplemented("not implemented, yet!")

        
        
    
    