#!/usr/bin/python
#-*- coding:utf-8 -*-

import json
import traceback
from .errors import ApiError, ApiException
from . import method

app_config=None

class FILTER():

    def __init__(self, config):
        self.config = config
        global app_config 
        app_config = config


    def __call__(self, environ, start_response):
        path_info = environ['PATH_INFO']
        method = self.get_method(path_info)
        if not method:
            result = {
                'status': 1,
                'message': 'Method not found'
            }
            return self.response(start_response, result)

        try:
            body = environ['wsgi.input'].read()

            if body is None or body == "":
                param = self.parse_querystring(environ.get('QUERY_STRING'))
                #param = None
            else:
                param = json.loads(body)

            result = {
                'status': 0,
                'message': 'Success'
            }
            
            method_return_value = method(self.config,param)
            if type(method_return_value) == dict:
                for key in method_return_value:
                    result[key] = method_return_value[key]
            else:
                result["result"] = method_return_value

        except (ApiError, ApiException), e:
            result = {
                'status': e.code,
                'mesage': e.message,
                'details': e.details,
            }
        except Exception, e:
            traceback.print_exc()
            result = {
                'status': 2,
                'message': 'System Internal Error',
                'details': str(e)
            }
        return self.response(start_response, result)



    def get_application(self):
        return self


    def parse_querystring(self,querystring):
        #from urllib import unquote
        params = {}
        if querystring is not None and len(querystring) > 0:
            #querystring=unquote(querystring)
            strs = querystring.split('&')
            for s in strs:
                p = s.split('=')
                params[p[0]] = '='.join(p[1:])     
        return params


    def get_method(self, path_info):
        dirs = path_info.split('/')
        if len(dirs) < 2:
            return None

        method_name = dirs[1]
        if hasattr(method, method_name):
            return getattr(method, method_name)

        return None


    def response(self, start_response, data):
        if type(data) in [dict, list]:
            final_data = [json.dumps(data)]
        elif type(data) is str:
            final_data = [data]
        else:
            final_data = [str(data)]

        start_response('200 OK', [('Content-Type', 'application/json')])

        #from dbsessions import cleanup_mysql_session
        #cleanup_mysql_session()

        return final_data
