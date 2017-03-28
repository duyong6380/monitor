#!/usr/sbin/env python
# -*- coding: utf-8 -*-

import urllib2 as url
import sys
import json
import codecs
sys.path.append("../")
from aoam_common import log

s_json_path = "/tmp/af_data/"

def send_json(data):
    ''''''
    filename = s_json_path +data['基本']['设备ID']+'_'+data['基本']['上报日期'].replace('/','') +'.json'
    fp = codecs.open(filename,'w+',"utf8")
    try:
        json_data = json.dumps(data,ensure_ascii=False,encoding='utf8') + "\n"
        fp.write(json_data)
    except:
        print sys.exc_info()
    fp.close()
    return True
    


if __name__ == '__main__':
    json_str = {"僵尸进程": "[python]"}
    json_str = json.dumps(json_str,ensure_ascii=False)#.encode('UTF-8')
    print json_str
  #  print type(json_str)
    send_json(json_str)


