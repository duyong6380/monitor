#!/usr/sbin/env python
#coding=utf-8

import commands
import sys
import os
import logProc as log
import getFilename as gfn
import common
import re
import file_proc
import shutil


UPLOAD_PARSE_LOCK_FILE = '/var/lock/upload_monitor.lock'
s_rootdir = "/var/duyong/"

class UploadParseMain(object):
    def __init__(self):
       self.com_handle =  self.init_func()
       self.root_dir = '/var/duyong/'
    def parse_entry(self):
        self.exec_func()
        self.exit_func()
    def exit_func(self):
        pass
    def exec_func(self):
        '''���ƶ����ص��ļ����н�������ں�������Ҫ�������£�
        1����ѹ����
        2�����ÿ��Ŀ¼������Ӧ�Ľ����������н���
        '''
        dir_list_info = {}
        dir_list_info = gfn.GetDirInfo(s_rootdir)
        #print dir_list_info
        for dir_key,dir_value in dir_list_info.items():
            try :
                self.parse_one_dir_file(dir_key,dir_list_info)
            except:
                log.error("func_name[exec_func]ִ�д���" )
                return False
        return True		


    def get_data_from_cloud(self):
        ''' ���ƶ˻�ȡ��Ҫ����������,��ʱ����'''
        pass
    def check_db_table_create(self):
        ''''''
        pass
        
    def init_func(self):
        '''ִ�н����ĳ�ʼ����������Ҫ�������£�
        ����ƶ��Զ���ȡ������Ҫ����������
        ������Ӧ�����ݿ��Ƿ��Ѿ�����
        '''
        self.get_data_from_cloud()
        self.check_db_table_create()
        com_handle = common.Common()
        return com_handle
            

    def parse_one_dir_file(self,dir_key ,dir_list_info):
        '''����һ��Ŀ¼�µ��ļ�'''
        for dirname in dir_list_info[dir_key]:
            FileList = []
            #print '-------FileList:',FileList
            
            print dirname 
            if dir_key != 'L05info':
                return True
            print dir_key 
            
            list_file = os.listdir(dirname)
            print 'list_file:%s , dirname:%s' %(list_file,dirname)
            new_file = file_proc.merge_mutil_file_to_one(dirname ,list_file)
            if len(new_file) == 0 :
                return False
                
            print 'new_file:',new_file	
            print dirname
            
            for file in new_file:
                FileList.append(os.path.join(dirname,file))

            try :
                print 'FileList:',FileList
                self.com_handle.common_parse_hook(FileList,dir_key)
                self.com_handle.delTempFile(FileList)
                '''
                if dir_key == 'L05info':
                    sys.exit(1)
                '''    
            except:
                print "��[%s]����" %(dir_key)
                sys.exit(1)
        return True
        
# ���ļ���ʵ�ֽ��̵���, ��֤��������, ����Ѿ��н��̵��û�û�˳����ͻ��˳�
# func          : ��ץ�쳣�Ĳ���
def single_process_run(func):
	'''��ץ�ļ����쳣���ж��Ƿ񵥽���'''
	global UPLOAD_PARSE_LOCK_FILE
	
	try:
		import fcntl
		f = open(UPLOAD_PARSE_LOCK_FILE, 'w')
		fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
	except Exception, e:
		f.close()
		func_name = func.__name__
		log.error('func_name:%s �Ѿ�����һ��ʵ��������' %func_name)
		sys.exit(1)
	func() 
	fcntl.flock(f, fcntl.LOCK_UN)
	f.close()
    
def main():
    '''������ؽ������������'''
    parse_handle = UploadParseMain()
    single_process_run(parse_handle.parse_entry)

if __name__ == '__main__':
	main()
