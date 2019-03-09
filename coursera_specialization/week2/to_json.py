import functools
import json

# def to_json(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         res_str = ''
#         if type(result) == dict:
#             res_str += '{'
#             for key, val in result.items():
#                 res_str += "\"%s\": %s, " % (key, val)
#             if res_str[-1] != '{':
#                 res_str = res_str[:-2]
#             res_str += '}'
#         elif type(result) == list:
#             res_str += '['
#             for el in result:
#                 if type(el) == type(res_str):
#                     el = "\'%s\'" % el
#                 res_str += "%s, " % el
#             if res_str[-1] != '[':
#                 res_str = res_str[:-2]
#             res_str += ']'
#         elif type(result) == str and not result:
#             res_str += "\"\""
#         else:
#             res_str += str(result)
#         res_str = res_str.replace('True', 'true')
#         res_str = res_str.replace('False', 'false')
#         res_str = res_str.replace('None', 'null')
#         return res_str
#     return wrapper

def to_json(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        return json.dumps(result)
    return wrapped
