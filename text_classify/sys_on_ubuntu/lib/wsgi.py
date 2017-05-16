#!/usr/bin/env python

import os
from paste.deploy import loadapp

CWD = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(os.path.dirname(CWD), 'etc', 'production.ini')

application = loadapp('config:%s' % config_file)
