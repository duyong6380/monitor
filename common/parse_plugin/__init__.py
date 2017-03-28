#!/usr/bin/env python
# -*- coding: utf-8 -*-


#��ģ����Ҫ���ڵ�����Ӧ��ҵ����ִ�в���

modules_name = ['L05parse']
import L05parse 

import sys
sys.path.append("../")
from aoam_common import (log,get_status)
from config import ROOT_DIR as ROOT_PATH

def plugin_init():
    '''
    '''
    return True


def plugin_run(date):
    '''
         breief:��Ҫ�ǿ���ģ�������
    '''
    if int(get_status()) != 2:
        return True
    
    s_path = os.path.join(ROOT_PATH,'/saas/data')
    for module in modules_name:
        try:
            eval(module).run()
        except Exception,err:
            log("run module %s failed,err %s" %(module,err))
            return False
    return True 
