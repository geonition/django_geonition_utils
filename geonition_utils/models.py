from datetime import datetime
from django.db import models
from django.conf import settings
from django.utils import simplejson as json
from geonition_utils.json import get_value_types
from manager import MongoDBManager

import types
    
class JSON(models.Model):
    """
    This model provides mongodb extensions
    for json text field to query key value
    pairs.
    """
    collection = models.CharField(max_length=30)
    json_string = models.TextField()
    
    mongodb = MongoDBManager()
    
    def save(self, *args, **kwargs):
        super(JSON, self).save(*args, **kwargs)
        
        #do nothing if USE_MONGODB False
        if getattr(settings, "USE_MONGODB", False):
            insert_json = json.loads(self.json_string)
            JSON.mongodb.save(insert_json,
                              self.id,
                              collection = self.collection)
    
    def delete(self, *args, **kwargs):
        super(JSON, self).delete(*args, **kwargs)
        
        #do nothing if USE_MONGODB False
        if getattr(settings, "USE_MONGODB", False):
            JSON.mongodb.remove(self.id)
      
    def json(self):
        """
        This function returns a dict representation
        of itself
        """
        return json.loads(self.json_string)
     
    #TODO change the name of this function to something more descriptive
    # get conflicts with model get function
    def get(self, key, default=None):
        try:
            return json.loads(self.json_string).get(key, default)
        except KeyError:
            return default
    
    def remove_values(self, keys):
        """
        This function takes an array of keys and
        removes them from the json string and
        saves the object
        """
        json_dict = json.loads(self.json_string)
        
        for key in keys:
            try:
                del json_dict[key]
            except KeyError:
                pass
            
        self.json_string = json.dumps(json_dict)
        self.save()
        
    def get_fields(self):
        """
        This function returns a dict where the key
        is the field name and the value the type of
        the field, the type of the field is described
        with the help of input types in html 5 specification.
        
        This function shows the key value type of one
        JSON
        """
        json_dict = json.loads(self.json_string)
        fields_dict = get_value_types(json_dict)
        
        return fields_dict
        
    def __unicode__(self):
        return self.json_string
    
    
class TimeD(models.Model):
    """
    This model brings functionality to
    query data that was 'valid' or
    existing at a certain time.
    """
    create_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(null=True)
    
    def expire(self):
        self.expire_time = datetime.today()
        self.save()
    
    def valid(self, time):
        """
        This function tests if this object was valid
        during the given time.
        """
        if self.create_time <= time:
            if self.expire_time == None:
                return True
            elif self.expire_time >= time:
                return True
            else:
                return False
        
    def get_fields(self):
        return {'time.create_time': 'string',
                'time.expire_time': 'string'}
        
    def __unicode__(self):
        return u'create time %s expire time %s' % (self.create_time, self.expire_time)
    