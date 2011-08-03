from pymongo import Connection
from django.db.models import Manager
from query import MongoDBQuerySet

import settings

class MongoDBManager(Manager):
    """
    This manager includes functions
    to handle mongodb crud functionality.
    It combines the django model queries with
    information in mongodb.
    """

    used_for_related_fields = True
    
    
    def __init__(self, collection_name = 'collection'):
        super(MongoDBManager, self).__init__()
        
        self.collection_name = collection_name
        
    def get_query_set(self):
        return MongoDBQuerySet(self.model,
                               using=self._db,
                               collection_name=self.collection_name)

    #general connect and disconnect functions
    def _connect(self,
                collection_name = 'collection'):
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
        database_name = getattr(settings, "MONGODB_DBNAME", 'softgis')

        self.connection = Connection(database_host, database_port)
        self.database = self.connection[database_name]
        self.collection = self.database[self.collection_name]
        
    def _disconnect(self):
        """
        This function disconnects from the mongodb database.
        """
        self.connection.disconnect()
        
    #MongoDB insert functions and update functions
    def save(self, json_dict, identifier):
        """
        This function saves the jsondict and gives
        it the given identifier.
        """
        self._connect(collection_name=self.collection_name)
        json_dict['_id'] = int(identifier)
        self.collection.save(json_dict)
        self._disconnect()
    
    #MongoDB remove functions
    def remove(self, identifier):
        """
        This functions removes the document with the given
        identifier from the collection.
        """
        self._connect(collection_name=self.collection_name)
        self.collection.remove(identifier)
        self._disconnect()
        
    #MongoDB query
    def find(self, spec=None):
        return self.get_query_set().find(spec)
        
    def find_range(self, key, min, max):
        return self.find({key: {"$gte": min, "$lte": max}})


        