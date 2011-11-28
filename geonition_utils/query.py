from django.db.models.query import QuerySet
from pymongo import Connection
from django.conf import settings

class MongoDBQuerySet(QuerySet):
    """
    QuerySet to handle mongodatabase queries
    """
    
    ### Methods overloaded from QuerySet ###
    def __init__(self,
                 model=None,
                 query=None,
                 using=None,
                 collection_name='collection'):
        
        super(MongoDBQuerySet, self).__init__(model=model,
                                              query=query,
                                              using=using)
        
        self.connection = None
        self.database = None
        self.collection = None
        self.is_connected = False
        self.collection = collection_name
        
        self._connect()
    
    def __del__(self):
        #super(MongoDBQuerySet, self).__del__()
        
        self._disconnect()
    
    #general connect and disconnect functions (also in Manager not DRY)
    def _connect(self):
        """
        Helper function to connect to
        mongodb
        
        The function connects to MongoDB as set in
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
        self.collection = self.database[self.collection]
        self.is_connected = True
    
    def _disconnect(self):
        """
        Helper function to disconnect from
        mongodb.
        """
        self.connection.disconnect()
        
        
    #MongoDB query
    def find(self, spec=None):
        """
        This function returns a queryset including
        those objects that has the given key value pair.
        
        The spec is moved directly to mongodb for querying.
        """
        mdb_cursor = self.collection.find(spec)
        ids = []
        for json_obj in mdb_cursor:
            if(json_obj != None):
                ids.append(json_obj['_id'])
        
        return super(MongoDBQuerySet, self).filter(id__in = ids)
    
    def find_exact(self, key, value):
        """
        This function will retrieve all entries that
        has the key with the exact value of value
        """
        return self.find({key: value})
        
    def find_range(self, key, min, max):
        """
        This functions returns a queryset with the objects that
        includes a key with a value between min and max.
        """
        return self.find({key: {"$gte": min, "$lte": max}})
        
    def find_min(self, key, min):
        """
        This function finds the entries that key is at
        minumum min
        """
        return self.find({key: {"$gte": min}})
        
    def find_max(self, key, max):
        """
        This function finds the entries that key is at
        maximum max
        """
        return self.find({key: {"$lte": max}})
        
