from pymongo import Connection
from django.db.models import Manager
from query import MongoDBQuerySet
from django.conf import settings

class MongoDBManager(Manager):
    """
    This manager includes functions
    to handle mongodb crud functionality.
    It combines the django model queries with
    information in mongodb.
    """

    used_for_related_fields = True
    
    def get_query_set(self, collection='collection'):
        """
        To make the manger more fale safe this function
        returns a normal django queryset if mongodb is
        not in use.
        """
        if getattr(settings, "USE_MONGODB", False):
            return MongoDBQuerySet(self.model,
                                   using=self._db,
                                   collection_name=collection)
        else:
            #return a django QuerySet if MongoDB not in use
            return super(MongoDBManager, self).get_query_set()
        

    #general connect and disconnect functions
    def _connect(self,
                collection = 'collection'):
        """
        This function connects to MongoDB as set in
        the settings.py file.
        
        MONGODB_HOST = host to connect to
        MONGODB_PORT = port to use for connection
        MONGODB_DBNAME = name of database
        
        The collection name is model based and defined in the model.
        """
        #get connection values from settings
        database_host = getattr(settings, "MONGODB_HOST", 'localhost')
        database_port = getattr(settings, "MONGODB_PORT", 27017)
        database_name = getattr(settings, "MONGODB_DBNAME", 'geonition')
        database_username = getattr(settings, "MONGODB_USERNAME", '')
        database_password = getattr(settings, "MONGODB_PASSWORD", '')
        
        self.connection = Connection(database_host, database_port)
        self.database = self.connection[database_name]
        self.database.authenticate(database_username, database_password)
        self.collection = self.database[collection]
        
    def _disconnect(self):
        """
        This function disconnects from the mongodb database.
        """
        self.connection.disconnect()
        
    #MongoDB insert functions and update functions
    def save(self, json_dict, identifier, collection='collection'):
        """
        This function saves the jsondict and gives
        it the given identifier.
        """
        self._connect(collection=collection)
        json_dict['_id'] = int(identifier)
        self.collection.save(json_dict)
        self._disconnect()
    
    #MongoDB remove functions
    def remove(self, identifier, collection='collection'):
        """
        This functions removes the document with the given
        identifier from the collection.
        """
        self._connect(collection_name=collection)
        self.collection.remove(identifier)
        self._disconnect()
        
    #MongoDB query
    def find(self, spec=None):
        return self.get_query_set().find(spec)
        
    def find_range(self, key, min, max):
        return self.find({key: {"$gte": min, "$lte": max}})


        
