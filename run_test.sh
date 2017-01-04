#!/usr/bin/env bash

LOGS=$(mktemp)
nosetests --with-coverage --cover-package=pycwl 2> $LOGS
cat $LOGS
grep pycwl $LOGS | awk '{ print "TOTAL: "$4; }'
TEST=$(grep FAILED $LOGS)
rm $LOGS
if [[ ! -z $TEST ]]; then echo "Tests failed." && exit 1; fi
exit 0
