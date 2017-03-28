#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import time
import datetime
from aoam_base_setting import *
from config import (read_config,write_config)

g_forground = False
g_date_list = []
g_filename_list = []

def is_download_enable():
    '''
        brief:获取是否允许下载的开关
    '''
    return read_config('enable')

def is_download_expire():
    '''
        brief:上次下载日期是不是今天
    '''
    today = get_now_date()
    last_date = read_config('last_date')
    if int(today) <= int(last_date):
        return False
    return True
    
def get_before_day(curr_day, n):
    """
    Breif: 获取前n天或后n天的日期
    args:
        curr_day，当前的日期形式为 20151214
        n, 当n为负数时表示前n天
            当n为正数时表示后n天
    Returns: 返回''表示参数错误
            res_day，表示返回日期
    """
    if not isinstance(n, int) \
        or len(curr_day) != DATE_LEN \
            or not curr_day.isdigit():
        return get_now_date()

    try:
        the_day = datetime.datetime(
            int(curr_day[0:4]),
            int(curr_day[4:6]),
            int(curr_day[6:8])) + datetime.timedelta(days=n)
       # the_day = datetime.datetime.now() + datetime.timedelta(days=n)
        the_day = the_day.strftime('%Y%m%d')
        return the_day
    except Exception, e:
        log(e)
        return get_now_date()    

def get_date_list(date):
    '''
        brief:获取日期列表
    '''
    today = int(get_now_date())
    ##获取后一天的日期才能下载
    last_date = get_before_day(date,1)
    date_list = []

    while(today > int(last_date)):
        date_list.append(last_date)
        last_date = get_before_day(last_date,1)

    g_date_list = date_list
    return date_list
    
               
    
def get_need_filenames(last_date):
    '''
        brief:根据上次的日期，获取需要处理的日期文件
    '''
    date_list = get_date_list(last_date)
    if not date_list:
        return False
     
    remote_ip_list = '_20.10.1.37'
    file_pre = 'file_data_'
    filelist = []
    for date in date_list:
        file_name = file_pre + date + remote_ip_list + '.tar.gz' 
        filelist.append(file_name)
    g_filename_list = filelist
    return filelist

def get_local_root_path():
    '''
    '''
    return FTP_INFO['localdir']
    
def get_last_date():
    '''
        brief:获取上次下载的日期
    '''
    return read_config('last_date') 

    
def get_status():
    '''
        brief：获取下载状态
    '''
    return read_config('status')  
    
def set_status(value):
    '''
        brief: 设置下载状态
    '''
    return write_config('status',value)

def set_last_date(value):
    '''
    '''
    return write_config('last_date',value)

def get_now_date():
    """
    Breif: 获取当前系统日期
    Returns: 20151020 形式的日期
    """
    return time.strftime("%Y%m%d", time.localtime(time.time()))
	
def set_run_forground(forground):
    """
    Breif: 设置前台运行标记
    Args: forground, True:前台运行; False:后台巡行
    """
    global g_forground
    g_forground = forground


def is_run_forground():
    """
    Breif: 是否前台运行
    Returns: g_forground,Ture,前台运行; False，后台运行
    """
    return g_forground

def log(*args):
    """
    Breif: 打印错误信息，并存日志到LOG_PATH
    Args: 输出信息
    """
    args = [time.strftime('%Y-%m-%d %H:%M:%S') + ':'] + list(args)
    if is_run_forground() or DEBUG == 1:
        print(*args)
    log_path = LOG_PATH + get_now_date() + '.logfile'
    if os.path.isfile(log_path) and os.path.getsize(log_path) > LOG_MAX_SIZE:
            # 日志大小超限，停止记录日志
            return
    with open(log_path, 'a') as f:
        f.writelines("\t".join(str(v) for v in args) + '\n')

if __name__ == '__main__':  
    #today = get_now_date()
    log(get_date_list('20170306'))