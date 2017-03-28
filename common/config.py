#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser

CONFIG_BASE_DIR = '/home/duyong/aoam_test/common/'
config_name = CONFIG_BASE_DIR + 'config.ini'

g_config_handle = 0

def init_config(filename):
    '''
        brief:初始化配置文件
        return: 配置文件句柄
    '''
    try:
        config = ConfigParser.ConfigParser()
        config.read(config_name)
    except Exception,err:
        log("配置文件初始化失败")
        return False
    return config

def read_config(key,section='info'):
    ''''''
    if not g_config_handle:
       init_config(config_name) 
    
    return g_config_handle.get(section,key)
          
def write_config(key,value,section='info'):
    '''
    '''
    if not g_config_handle:
       init_config(config_name)
    try:
        g_config_handle.set(section,key,value)
        g_config_handle.write(open(config_name,"wb"))
    except  Exception,err:
        log("write config [%s] failed",sys.exc_info() %key)
        return False
    return True
         
    
g_config_handle = init_config(config_name)