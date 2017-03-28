#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import tarfile
from aoam_common import (get_status,set_status,\
                        g_filename_list,get_need_filenames,\
                        get_local_root_path,log,get_last_date)
                        
s_filename_list = g_filename_list
s_root_path = ""

def init():
    '''
    '''
    return True

def unrar(file_list):
    '''
    '''
    print 's_root_path:',s_root_path
    for filename in file_list:
        if os.path.exists(filename) == False:
                continue
        try:
            tar = tarfile.open(filename)
            for names in tar.getnames():
                tar.extract(names,path=s_root_path)
            tar.close()
        except Exception,err:
            log("untar file failed,err:",sys.exc_info())
            return False
            
    return True

def get_filename_list():
    '''
        brief:获取需要解压的文件名列表
    '''
    if not s_filename_list:
        last_date = get_last_date()
        if not last_date:
            return False
    print last_date
    return get_need_filenames(last_date)
        
def get_uncompress_file_list():
    '''
        brief:获取需要解压的具体文件路径列表
    '''
    global s_root_path
    global s_filename_list
    
    file_list = []
    
    s_filename_list = get_filename_list()
    if not s_filename_list:
        return False
        
    s_root_path = get_local_root_path()
   
    for file in s_filename_list:
        filename = os.path.join(s_root_path,os.path.basename(file))
        if os.path.exists(filename) == False:
            continue
        file_list.append(filename)
        
    return file_list
        
    
def run():
    '''
    '''
    if int(get_status()) != 1:
        return True
        
    uncompress_file_list = get_uncompress_file_list()
    if not uncompress_file_list:
        log("uncompress file list is not exists ,module exit")
        return True
    log("current need uncompress file list is",uncompress_file_list)
    ret = unrar(uncompress_file_list)
    if ret == False:
       return False
       
    set_status(2)
    return True
        
if __name__ == "__main__":
    init()
    run()
