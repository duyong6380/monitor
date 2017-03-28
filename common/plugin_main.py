#!/usr/bin/env python
# -*- coding: utf-8 -*-

#本模块主要用于调用相应的业务插件执行操作

from parse_plugin import plugin_run
from aoam_common import (get_status,get_last_date,log)

def init():
    '''
    '''
    return True


def run():
    '''
         breief:主要是控制模块的运行
    '''
    if int(get_status()) != 2:
        return True
    
    s_date_list = get_last_date()
    for date in s_date_list:
        if not plugin_run(date):
            log("date %s parse failed,err ",sys.exc_info())
            return False
    return True 

if __name__ == "__main__":
    init()
    run()