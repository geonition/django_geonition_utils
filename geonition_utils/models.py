from django.db import models
from django.conf import settings
from django.utils import simplejson as json
from manager import MongoDBManager
from datetime import datetime

class JSON(models.Model):
    """
    This model provides mongodb extensions
    for json text field to query key value
    pairs.
    """
    collection = models.CharField(max_length=20)
    json_string = models.TextField()
    
    mongodb = MongoDBManager()
    
    def save(self, *args, **kwargs):
        super(JSON, self).save(*args, **kwargs)
        
        #do nothing if USE_MONGODB False
        if getattr(settings, "USE_MONGODB", False):
            insert_json = json.loads(self.json_string)
            JSON.mongodb.save(insert_json, self.id)
    
    def delete(self, *args, **kwargs):
        super(JSON, self).delete(*args, **kwargs)
        
        #do nothing if USE_MONGODB False
        if getattr(settings, "USE_MONGODB", False):
            JSON.mongodb.remove(self.id)
      
    def json(self):
        return json.loads(self.json_string)
        
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
        
        super(TimeD, self).save()
        
    
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
        
    
    