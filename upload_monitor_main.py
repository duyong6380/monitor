#!/usr/sbin/env python
#coding:UTF-8


import sys

from common import module_exec
from common.aoam_daemon import daemon
from common.aoam_common import *
import getopt

s_fh = 0

UPLOAD_PARSE_LOCK_FILE = '/var/lock/upload_monitor.lock'

def usege():
    """
    Breif: 输出帮助信息
    """
    print('-af    run forground...')
    print("-h     please input '-af' enter debug mode...")


def cmd_line_parse(argv):
    """
    Breif: 命令行解析，-a,-f,-af进入前台模式
    """
    if len(argv) > 1:
        try:
            opts, args = getopt.getopt(argv[1:], 'afh', ['help'])
        except getopt.GetoptError:
            usege()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-a', '-f'):
                set_run_forground(True)
            elif opt in ('-h', '--help'):
                usege()
                sys.exit(1)
                
                
def aoam_module_load():
    ''''''
    log("module load start")
    
    try:
        module_exec("")
    except Exception,err:
        log("module init failed ")
        sys.exit(1)
        
def run_main():
    '''
    brief:主要运行函数和控制逻辑，负责初始化和执行模块加载函数
    '''
    try:
        module_exec("",1)
    except Exception,err:
        log("module running failed ")
        sys.exit(1)

def single_process_run():
    '''只允许单实例进行'''
    global s_fh
    try:
        import fcntl
        s_fh = open(UPLOAD_PARSE_LOCK_FILE, 'w')
        fcntl.flock(s_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print('another instance is running...')
        sys.exit(1)

def aoam_daemon():
    """
    Breif: 进程daemon化,并创建pid文件
    """
    global s_fh
    if not is_run_forground():
        daemon()
    #  写入pid文件进程号
    try:
        pid = str(os.getpid())
        s_fh.write("%s\n" % pid)
        s_fh.flush()
    except IOError:
        sys.exit(1)
        
def main(argv):
    '''主函数执行'''
    
    cmd_line_parse(argv)
    #单实例运行
    single_process_run()
    
    #后台运行
    aoam_daemon()
    
    #模块加载并初始化
    aoam_module_load()
    
    try:
        run_main()
    except Exception, err:
        log('saas_mainloop error: ', err)
        return 1
    return 0


if __name__ == '__main__':
    ret = main(sys.argv)
    sys.exit(ret)
