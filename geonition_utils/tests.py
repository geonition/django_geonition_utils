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

class JSONModelTest(TestCase):
    """
    This test tests the functionality of
    the JSON model
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
            "number": 1,
            "boolean": True,
            "null": None,
            "object": {
                "nested": False
            },
            "array": ["no","yes"]    
        }
        
        json_mo1 = JSON(collection='test',
                        json_string=json.dumps(self.test_json_1))
        json_mo1.save()
        json_mo2 = JSON(collection='test',
                        json_string=json.dumps(self.test_json_2))
        json_mo2.save()
    
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
            
            result = JSON.mongodb.find({"id": 2})
            self.assertEquals(result[0].json(),
                              self.test_json_2,
                              "query with id did not return the right object")
            
            result = JSON.mongodb.find({"boolean": True})
            self.assertEquals(result[0].json()["boolean"],
                              True,
                              "query with boolean did not return correct result")
            
            result = JSON.mongodb.find({"boolean": False})
            self.assertEquals(result[0].json()["boolean"],
                              False,
                              "query with boolean did not return correct result")
            
            result = JSON.mongodb.find({"object": {"nested": False}})
            self.assertEquals(result[0].json()["object"],
                              {"nested": False},
                              "query a nested object did not return the right result")
            
            result = JSON.mongodb.find({"array": ["no", "yes"]})
            self.assertEquals(result[0].json()["array"],
                              ["no", "yes"],
                              "query a array did not return the right object")
            
            result = JSON.mongodb.find_range('number', 0, 1)
            self.assertLessEqual(result[0].json()["number"],
                                 1.1,
                                 "querying with no input does not return 2 json objects")
            self.assertGreaterEqual(result[0].json()["number"],
                                    -0.1,
                                    "querying with no input does not return 2 json objects")
    
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
        
        