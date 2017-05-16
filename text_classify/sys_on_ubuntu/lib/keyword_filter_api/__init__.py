#!/usr/bin/python
#-*- coding:utf-8 -*-

from .keyword_filter import FILTER

def main(global_config, **settings):
    keyword_filter = FILTER(settings)
    return keyword_filter.get_application()
