#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os 
from  ftplib import FTP
from aoam_base_setting import FTP_INFO
from aoam_common import (log,get_now_date,is_download_enable,\
                        is_download_expire,get_need_filenames,\
                        get_status,set_status,\
                        get_last_date,set_last_date)



s_ftp_info = {}
s_conn = FTP()

def ftp_login(host,username,password,port=21,timeout=300):
    '''
        brief:ftp登录
    '''
    global s_conn

    try:
     #   s_conn.set_debuglevel(2)
        s_conn.connect(host,port,timeout)
        s_conn.login(username,password)
    except Exception,err:
        log("ftp server login failed:",sys.exc_info())
        return False
    log(s_conn.welcome)
    return True


def get_file(ftp_path,local_path='.'):
    ''''''
    global s_conn
    ftp_login(s_ftp_info['host'], s_ftp_info['username'],\
               s_ftp_info['password'],s_ftp_info['port'],\
               s_ftp_info['timeout'])
    
    ftp_path = ftp_path.rstrip('/')   
    file_name = os.path.basename(ftp_path)
    local_file = os.path.join(local_path,file_name)
    ftp_path = os.path.join(s_ftp_info['remote_root_dir'] , ftp_path)
    
    #如果本地路径是目录，下载文件到该目录
    print 'ftp_path',ftp_path
    lsize = 0L
    lfile = local_file
    if os.path.exists(lfile):
       lsize = os.stat(lfile).st_size
       f = open(lfile, 'ab')
    else:
       f = open(lfile, 'wb')
    try:   
        s_conn.retrbinary("RETR %s" %ftp_path, f.write, rest=lsize)
    except:
        print sys.exc_info()
    #s_conn.set_debuglevel(0)

    f.close()

    return True
    
def close():
    ''''''
    global s_conn
    if s_conn :
        s_conn.quit()    
       

def init():
    '''
        Brief:初始化一些配置
    '''
    log("download init====")
    global s_ftp_info
    s_ftp_info['username'] = FTP_INFO['username']
    s_ftp_info['password'] = FTP_INFO['password']
    s_ftp_info['host'] = FTP_INFO['host']
    s_ftp_info['port'] = FTP_INFO['port']
    s_ftp_info['timeout'] = FTP_INFO['timeout']
    s_ftp_info['localdir'] = FTP_INFO['localdir']
    s_ftp_info['remote_root_dir'] = FTP_INFO['remote_root_dir']
    
def download(filenames):
    '''
       brief:从云端开始下载数据
    '''
    
    for file in filenames:
        if get_file(file,s_ftp_info['localdir']) == False:
            return False
            
        last_date = file.split('_')[2]
        set_last_date(last_date)
    close()
    return True
    
def is_can_download_check():
    '''
        确定是否可以允许下载，进行条件检查
        true: 能下载，false 不能下载
    '''
    if not is_download_enable():
        return False
    if int(get_status()) != 0:
        return False
    return True
        
    
def run():
    '''
        主要是执行FTP下载任务
    '''
    if not is_can_download_check():
        return True
    download_file_list = get_need_filenames(get_last_date())
    if not download_file_list:
        log("have no file to download ,exit")
        return True
    
    log("need download file list:",download_file_list)
    if download(download_file_list) == False:
        close()
        return False
    log("==============download success====")
    #下载完成之后更新下载状态
    set_status(1)
    return True
 
if __name__ == '__main__':
   init()
   run()
