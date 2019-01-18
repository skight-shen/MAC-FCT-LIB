#!/bin/sh
export PYTHONPATH='/Library/python-sequencer'
WPATH=`dirname $0`
#python /Library/python-sequencer/x527/loggers/logger.py --disable_pudding
python ${WPATH}/stateMachine.py