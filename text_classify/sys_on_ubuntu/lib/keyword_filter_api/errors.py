#!/usr/bin/python
#-*- coding:utf-8 -*-

class ApiError(Exception):
    def __init__(self, code, message, details=None):
        self.code = code
        self.message = message
        self.details = details

class ApiException(Exception):
    def __init__(self, code, message, details=None):
        self.code = code
        self.message = message
        self.details = details
