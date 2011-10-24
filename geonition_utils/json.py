"""
This file includes helper functions to handle json
or dict related processing.
"""
import types

def create_key_set(json_dict):
    """
    This function returns a set of keys
    created according to the keys and
    sub dictionaries found in the given
    json_dict. If there are nested objects
    the keys will be presented in the following
    form: key1.key2 etc..
    
    >>> d = {'some_val': 'string'}
    >>> d.update({'number': 2})
    >>> d.update({'boolean': True})
    >>> d.update({'object': {'string': 'hello world'}})
    >>> create_key_set(d)
    set(['boolean', 'some_val', 'number', 'object.string'])
    """
    key_set = set()
    
    for key, item in json_dict.items():
        if type(item) == types.DictType:
            temp_set = create_key_set(item)
            for header in temp_set:
                add_header = "%s.%s" % (key, header)
                key_set.add(add_header)
        else:
            key_set.add(key)
            
    return key_set


def get_value_list(json_dict, key_list):
    """
    Given the key_list this function returns
    a list of values that are can be found in
    the given json_dict. The not found values
    will be an empty string.
    
    
    >>> d = {'some_val': 'string'}
    >>> d.update({'number': 2})
    >>> d.update({'boolean': True})
    >>> d.update({'object': {'string': 'hello world'}})
    >>> ks = create_key_set(d)
    >>> kl = list(ks)
    >>> kl.sort()
    >>> print kl
    ['boolean', 'number', 'object.string', 'some_val']
    >>> rl = get_value_list(d, kl)
    >>> rl.sort()
    >>> print rl
    [True, 2, 'hello world', 'string']
    """
    
    value_list = []
    
    for key in key_list:
        
        keys = key.split(".")
        
        if len(keys) == 1:
            if json_dict.has_key(key):
                value_list.append(json_dict[key])
            else:
                value_list.append("")
        else:
            temp_key = ""
            
            for k in keys[1:]:
                if temp_key != "":
                    temp_key = temp_key + "." + k
                else:
                    temp_key = k
            
            if json_dict.has_key(keys[0]):
                temp_value_list = get_value_list(json_dict[keys[0]],
                                                 [temp_key])
            else:
                temp_value_list = get_value_list({},
                                                 [temp_key])
                
            value_list.extend(temp_value_list)
    
    return value_list

def get_value_types(json_dict):
    """
    This function returns another dict with the values
    changed to the type of the value. The values are defined
    according to JSON values and the following rules:
    http://www.json.org/
    
    >>> d = {'some_val': 'string'}
    >>> d.update({'number': 2})
    >>> d.update({'boolean': True})
    >>> d.update({'object': {'string': 'hello world'}})
    >>> get_value_types(d)
    {'boolean': True, 'some_val': 'string', 'number': 'number', 'object': 'object', 'object.string': 'hello world'}
    """
    value_type_dict = {}
    for key, value in json_dict.items():
        if type(value) == types.IntType or type(value) == types.FloatType:
            value_type_dict[key] = 'number'
        elif type(value) == types.StringTypes:
            value_type_dict[key] = 'string'
        elif type(value) == types.ListType:
            value_type_dict[key] = 'array'
        elif type(value) == types.DictType:
            value_type_dict[key] = 'object'
            
            #extend the value_type_dict with the values in the nested object
            nested_value_types = get_value_types(json_dict[key])
            for key_nested in nested_value_types.keys():
                nk = key + "." + key_nested
                value_type_dict[nk] = nested_value_types[key_nested]
                
        else:
            #the rest can be described as is the JSON encored will
            # change them e.g. true false null
            value_type_dict[key] = value
    
    return value_type_dict

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    