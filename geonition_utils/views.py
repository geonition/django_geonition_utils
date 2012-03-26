"""
This file contains view classes that can be used in other applications.
"""
from geonition_utils.http import HttpResponseNotImplemented
from django.views.generic import View

class RequestHandler(View):
    """
    This class should be inherited by the view
    classes to be used for implementing REST
    """
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
        
    def get_user_name(self,
                      request,
                      username = None):
        """
        This function will return the username / user-id of
        the user that sent the request. If the name cannot be resolved
        this function will return None.
        
        e.g.
        @me --> username of authenticated user
        None --> username of authenticated user
        """
        if username == '@me' or username == None:
            username = request.user.username
        
        return username

        
        
    
    