# -*- coding: utf-8 -*-
import json
import time
import fcntl

path = '/tmp/'

def SaveSnToJsonFile(data):
    if not isinstance(data,dict):
        raise TypeError
    with open(path+'mlbsn.json','w') as f:
        f.write(json.dumps(data))


# a = {'sn1':'123123121',
#      'sn2':'234234234',
#      'sn3':'345345345',
#      'sn4':'456456456'
#      }
#
# SaveSnToJsonFile(a)

# pwd = os.path.split(__file__)[0]
# config_file = os.path.join(pwd, 'Config.json')
# f = open(config_file, 'rU')
# config = json.load(f)
# f.close()



def CompareWithSn(sn):
    if not isinstance(sn,str):
        raise TypeError
    with open(path+'mlbsn.json','r') as f:
        fcntl.flock(f,fcntl.LOCK_EX)
        config = json.load(f)
    if '456456456'== config['sn4']:
        print '111111'
    else:
        print '22222'


CompareWithSn('asdasd')