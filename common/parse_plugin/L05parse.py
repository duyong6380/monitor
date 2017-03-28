#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os 
import re
import time
sys.path.append("../")
from aoam_common import log
from common import (get_need_file_list,uncompress,get_spec_dir,\
                    get_ini_sections,format_common_func)
from send_json import send_json as send_post

s_process_file = 'sys_info.txt'

key = 'L05info'
format_cb = {} ##展示在DP平台之前的格式化回调函数
preprocess_cb = {} ##预处理数据的回调函数

def init():
    '''
        brief:初始化配置，暂时只分配格式化回调函数
    '''
    global format_cb
    global preprocess_cb
    format_cb['BASE'] = format_base_callback
    format_cb['CPU'] = format_CPU_callback
    format_cb['MEM'] = format_MEM_callback
    preprocess_cb['BASE'] = process_base_section
    return True


def crash_time_format(dict_info):
    '''
    '''
    time_str = dict_info['crash_time']
    if len(time_str) == 1:
        time_str = "2012/02/14T23:48:41"
    
    if time_str.find('Crashed time:') != -1:
        time_str = time_str[len(" Crashed time"):].replace(' ','T')
        time_str = time_str.replace('-','/')
    dict_info['crash_time'] = time_str
    return dict_info
        
def process_base_section(dict_info):
    '''
        brief:基本信息中进行相应的格式转换或者是数据解析处理
    '''
    
    format_birth = dict_info['device_time']
  
    if format_birth.find("-") != -1:
        format_birth = format_birth.replace('-','/')
    else:
        birth_secds = time.mktime(time.strptime(format_birth, "%Y%m%d %H:%M:%S"))
        format_birth = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime(birth_secds))
    dict_info['record_date'] = format_birth.split(' ')[0]
    
    
    dict_info = crash_time_format(dict_info)
    print "after:crash_time:",dict_info['crash_time']
    
    if 'device_version' not in dict_info:
        dict_info['device_version'] = dict_info.pop('device_vervion')
        
    dict_info['run_time'] = int(dict_info['run_time'].split(' ')[0])
    dict_info['version'] = dict_info['device_version'].split(' ')[0]
    dict_info['major_version'] = dict_info['version'][0:5]
    
    hard_arr = dict_info.pop('hard_plat').split(' ')
    dict_info['硬件版本'] = hard_arr[0].split(':')[1]
    dict_info['硬件厂商'] = hard_arr[1].split(':')[1]
    dict_info['硬件型号'] = hard_arr[2].split(':')[1]
    dict_info['硬件AF型号'] = hard_arr[3].split(':')[1]
    
    dict_info['customer'] = dict_info['customer'].strip()
    
    return dict_info
    
def format_MEM_callback(dict_info):
    '''
    '''
    mem_key = {"mem_usage":"最小内存"}
    if 'mem_limit' in dict_info:
        dict_info.pop('mem_limit')
    
    dict_info = string_data_proc('mem_usage',dict_info)
  
    return format_common_func(dict_info,mem_key)
    
def string_data_proc(key,dict_info):
    '''
    '''
    if dict_info[key].find('[') != -1:
        re_list = re.findall('\[(.*)\]',dict_info[key])
        dict_info[key] = int(re_list[0])
        
    if isinstance(dict_info[key],str):
        if dict_info[key].find('Normal') != -1:
            dict_info[key] = 65536   
    return dict_info
    
def format_CPU_callback(dict_info):
    '''
    '''
    cpu_key = {"cpu_usage":"cpu"}
    
    dict_info = string_data_proc("cpu_usage",dict_info)
    return format_common_func(dict_info,cpu_key)

    
def get_use_sec(section):
    '''
        brief:只获取暂时能够显示在DP平台上的数据
    '''
    use_sections = ['BASE','CORE_DUMP','CPU','MEM','CORE_PROCESS','CORE_MODULE','CORE_CONF']
    new_section = []
    for name in section:
        if name in use_sections:
            new_section.append(name)
    return new_section
        
def get_need_process_sections(filename):
    '''
        brief:对配置文件中的段进行处理
    '''
    cf,section = get_ini_sections(filename)
    if not section:
       return False
        
    section = get_use_sec(section)
    log('sections:',section)
    return cf,section

def DP_format_process(dict_info):
    '''
        brief:在DP平台展示时，需要处理展示格式
    '''
    new_dict ={}
    
    for key,value in dict_info.items():
        if key not in format_cb:
            new_dict[key] = value
        else:
            new_dict[key] = format_cb[key](value)
    
    dict_info = {}
    for key,value in new_dict.items():
        dict_info[key_covert(key)] = value
    
    return dict_info
 
def key_covert(key):
    '''
    '''
    master_key_dict = {"BASE":"基本","softdog":"软狗","harddog":"硬狗",\
        "ZOMBIE":"僵尸进程","CORE_DUMP":"内存转储","MEM":"内存","STORAGE_CHECK":"存储设备",\
        "SMARTCTL":"硬盘寿命","CORE_PROCESS":"核心进程","CORE_MODULE":"核心模块","CORE_CONF":"核心配置",\
        "ABNORMAL_USER":"异常账户","OPENED_PORT":"开放端口","DCLOG_SIZE":"日志记录","sangfor_waf":"sangfor_waf",\
        "SSHD_INFO":"SSH访问记录","ALL_MODULE":"所有驱动","ALL_PROC":"所有进程"}
    for new_key,value in master_key_dict.items():
        if key == new_key:
            return value
    return key
        
def format_base_callback(dict_info):
    '''
        基本信息的转换
    '''
    base_key = {"dev_id":"设备ID","customer":"设备账户","hard_plat":"硬件平台","device_ip":"设备IP",\
        "crash_time":"最近宕机时间","run_time":"持续运行时间","device_time":"上报时间",\
        "device_plat":"设备硬件平台","storage_plat":"存储硬件类型","device_version":"全版本号",\
        "version":"版本号","major_version":"主版本号",\
        "record_date":"上报日期","flag":"存在异常","admin":"管理员入口"}
    return format_common_func(dict_info,base_key)
    
def process_subsection_info(sub_sec,cf):
    '''
        brief:处理字段信息
    '''
    dict_info = {}
    dict_info = dict(cf.items(sub_sec))
    if 'cnt' in dict_info:
        dict_info.pop('cnt')
    
    
    if sub_sec in  preprocess_cb:
       dict_info = preprocess_cb[sub_sec](dict_info)
        
    #log("dict_info",dict_info)
    return dict_info

def process(filename):
    '''
    '''
    cf,sections = get_need_process_sections(filename)
    if not sections :
        return False
    dict = {}
    for sub_sec in sections:
        dict[sub_sec] = process_subsection_info(sub_sec,cf)
    
    dict = DP_format_process(dict)
    if dict:
        send_post(dict)
    return True
    
      
def run(path):
    '''
    '''
    log("plugin [%s] start running" %key)
    
    file_path_list = get_need_file_list(path , key)
    
    save_dir = get_spec_dir(key)
    preproces_filename = os.path.join(save_dir,s_process_file)
    
    for file in file_path_list:
        if os.path.exists(preproces_filename) == True:
            os.unlink(preproces_filename)
            
        ret = uncompress(file,key,save_dir)
        if not ret:
            return False
        
        if not process(preproces_filename):
            return False
    return True

    
    
if __name__ == '__main__':
    init()
    path = "/var/duyong/saasdata/file_data/20170311"
    run(path)