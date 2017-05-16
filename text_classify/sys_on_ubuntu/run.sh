#!/bin/sh
bash stop.sh

#python wsgi.py $port 2>&1 &
sudo paster serve etc/production.ini test_app=$PWD

