#!/bin/sh
echo "==========kill blow process start=========="
ps -ef | grep etc/production.ini | grep test_app=$PWD
ps -ef | grep etc/production.ini | grep test_app=$PWD | awk '{print $2}' | xargs -i{} sudo kill -9 {}
echo "==========kill blow process end=========="


