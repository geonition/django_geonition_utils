"""
This file makes sure that the utils work correctly
"""
from django.test import TestCase
from django.conf import settings
from django.utils import simplejson as json
from django.contrib.auth.models import User
from models import JSON
from models import TimeD
from datetime import datetime

class UtilsTest(TestCase):
    """
    Tests the functionality of
    the utils.
    """
    
    def setUp(self):

        # test data as python dicts
        self.test_json_1 = {
            "id": 1,
            "some_key": "some_value",
            "number": 1,
            "boolean": False,
            "null": None,
            "object": {
                "nested": True
            },
            "array": [1,2,3,4,5]
        }
        self.test_json_2 = {
            "id": 2,
            "some_key": "some_value and other text",
            "number": 0,
            "boolean": True,
            "null": None,
            "object": {
                "nested": False
            },
            "array": ["no","yes"]    
        }
        self.test_json_3 = {
            "id": 3,
            "some_key": "some_value and other text",
            "number": 3,
            "boolean": True,
            "null": None,
            "object": {
                "nested": False
            },
            "array": ["no","yes"]    
        }
        
        self.json_mo1 = JSON(collection='test',
                        json_string=json.dumps(self.test_json_1))
        self.json_mo1.save()
        self.json_mo2 = JSON(collection='test',
                        json_string=json.dumps(self.test_json_2))
        self.json_mo2.save()
    
    def test_mongodb(self):
        # next version 1.4 of django supports changing settings in tests
        # modify this test to use USE_MONGODB=False
        # and then back to settings value
        
        #simple tests when mongodb is not in use
        result = JSON.mongodb.filter(collection='test')
        self.assertEquals(len(result),
                          2,
                          "Querying for collection 'test' does not return"
                          "2 results")
        
        
        
        #test key value queries only if mongodb is in use
        if getattr(settings, "USE_MONGODB", False):
            
            #query with empty
            result = JSON.mongodb.find()
            self.assertEquals(len(result),
                              2,
                              "querying with no input does not return 2 json objects")
            
            result = JSON.mongodb.find({})
            self.assertEquals(len(result),
                              2,
                              "querying with '{}' does not return 2 json objects")
            
            result = JSON.mongodb.find({"id": 1})
            self.assertEquals(result[0].json(),
                              self.test_json_1,
                              "query with id did not return the right object")
            self.assertEquals(len(result),
                              1,
                              "The query returned too many objects")
            
            result = JSON.mongodb.find({"id": 2})
            self.assertEquals(result[0].json(),
                              self.test_json_2,
                              "query with id did not return the right object")
            self.assertEquals(len(result),
                              1,
                              "The query returned too many objects")
            
            result = JSON.mongodb.find({"boolean": True})
            for obj in result:                
                self.assertEquals(obj.json()["boolean"],
                                  True,
                                  "query with boolean did not return correct result")
            
            result = JSON.mongodb.find({"boolean": False})
            for obj in result:
                self.assertEquals(obj.json()["boolean"],
                                  False,
                                  "query with boolean did not return correct result")
            
            result = JSON.mongodb.find({"object": {"nested": False}})
            for obj in result:
                self.assertEquals(obj.json()["object"],
                                  {"nested": False},
                                  "query a nested object did not return the right result")
            
            result = JSON.mongodb.find({"array": ["no", "yes"]})
            for obj in result:
                self.assertEquals(obj.json()["array"],
                                  ["no", "yes"],
                                  "query a array did not return the right object")
            
            result = JSON.mongodb.find_range('number', 0, 1)
            for obj in result:
                self.assertLessEqual(obj.json()["number"],
                                     1.1,
                                     "Range query did not work correctly")
                self.assertGreaterEqual(obj.json()["number"],
                                        -0.1,
                                        "Range query did not work correctly")
    
    def test_json_model(self):
        
        #test really long json, try to reproduce the index error
        json_dict = {}
        for i in range(7000):
            json_dict[str(i)] = "some string"
            
        json_str = json.dumps(json_dict)
        json_obj = JSON(collection='test',
                        json_string=json_str)
        json_obj.save()
        
        # test the supported fields of one json
        fields = self.json_mo1.get_fields()
        
        self.assertEquals(fields,
                          {u'object': 'object',
                           u'some_key': u'some_value',
                           u'object.nested': True,
                           u'number': 'number',
                           u'boolean': False,
                           u'array': 'array',
                           u'null': None,
                           u'id': 'number'},
                          "The get_fields function did not return the correct "
                          "result")       
        
    def test_timed_model(self):
        before_create_time = datetime.today()
        time = TimeD()
        time.save()
        valid_time = datetime.today()
        time.expire()
        time.save()
        after_expire_time = datetime.today()
        
        self.assertFalse(time.valid(before_create_time))
        self.assertTrue(time.valid(valid_time))
        self.assertFalse(time.valid(after_expire_time))
        