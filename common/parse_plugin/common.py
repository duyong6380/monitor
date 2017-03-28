#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import zipfile
import ConfigParser
sys.path.append("../")
from aoam_common import log
from aoam_base_setting import SAVE_PATH_DIR

s_save_path = SAVE_PATH_DIR

def get_dir_by_key(path , key):
    '''
    '''
    file_list = []
    for dir in os.listdir(path):
        if re.search(key, dir) is not None:
            file_list.append(os.path.join(path,dir))
    file_list = list(set(file_list))
    return  file_list

def get_filepath_by_dir(dir_info):
    '''
        brief:根据目录路径获取具体的文件路径
    '''
    file_path_list = []
    for dir in dir_info:
        for root,dirs,files in os.walk(dir):
            for filespath in files:
                file_path_list.append(os.path.join(root,filespath))
        file_path_list = list(set(file_path_list))
    return file_path_list

def get_need_file_list(path , key):
    '''
        根据根路径和key值获取解析的文件列表
    '''
    dir_info = get_dir_by_key(path,key)
    if not dir_info:
        log("current upload info is not exist info [%s]" %key)
        return True
    log("dir_info:", dir_info)
    file_info = get_filepath_by_dir(dir_info)
    if not file_info:
        log("current upload [%s] is  empty file list" %key)
        return True
    #log("file_info:",file_info)  
    return file_info

def format_common_func(dict_info,key_dict_info):
    '''
        格式装换通用函数
    '''
    new_dict = {}
    for key ,value in dict_info.items():
        if key not in key_dict_info:
            new_dict[key] = value
        else:
            new_dict[key_dict_info[key]] = value
    return new_dict
    
def unzip(file,path):
    '''
    '''
    try:
        fz = zipfile.ZipFile(file,mode='r')

        for file in fz.namelist():
            fz.extract(file,path)
        fz.close()
    except Exception,err:
        log("file:" + file + " unzip failed,err:",sys.exc_info())
        return False
    return True
        
def get_ini_sections(filename):
    '''
        brief:获取ini配置文件中的段
    '''
    try:
        cf = ConfigParser.ConfigParser()
        cf.read(filename)
        section = cf.sections()
    except Exception,err:
        log('get ini['+filename+'] section failed,err:',sys.exc_info)
        return False,False
    return cf,section
    
def untar(file,path,num=3):
    '''
    '''
    cmd = "tar xvf " + file + " --strip-components " +  str(num) + " -C " + path + " >>/dev/null"
    try:
        os.system(cmd)
    except Exception,err:
        log("file:[" + file + "] failed,err:",sys.exc_info())
        return False
    return True
    
def get_spec_dir(key):
    '''
    '''
    global s_save_path
    unzip_save_dir = os.path.join(s_save_path,key)
    log('tmp_unzip_save_dir:',unzip_save_dir)
    if os.path.exists(unzip_save_dir) == False:
        os.makedirs(unzip_save_dir)
    return unzip_save_dir
        
def uncompress(file,key,path):
    '''
        解压文件到指定目录
    '''
    if os.popen('file '+ file + '| grep "Zip archive"' ).read():
        ret = unzip(file,path)
    else:
        ret = untar(file,path)
    return ret
    
if __name__ == '__main__':
   dir = ['/var/duyong/saasdata/file_data/20170311/L05info_7.1']
   print get_filepath_by_dir(dir)