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

def get_data_from_cloud():
	''' ���ƶ˻�ȡ��Ҫ����������,��ʱ����'''
	pass
def check_db_table_create():
	''''''
	pass
	
def init_func():
	'''ִ�н����ĳ�ʼ����������Ҫ�������£�
	1�����ƶ��Զ���ȡ������Ҫ����������
	2�������Ӧ�����ݿ��Ƿ��Ѿ�����
	'''
	get_data_from_cloud()
	check_db_table_create()
	common.common_init()
	 	

def parse_one_dir_file(dir_key ,dir_list_info):
	'''����һ��Ŀ¼�µ��ļ�'''
	for dirname in dir_list_info[dir_key]:
		FileList = []
		#print '-------FileList:',FileList
		'''
		print dirname 
		if dir_key != 'L05info':
			return True
		print dir_key 
		'''
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
			
			common.common_parse_hook(FileList,dir_key)
			common.delTempFile(FileList)
			
		except:
			log.error("����ʧ��[%s]" %(dir_key))
			sys.exit(1)
	return True
	
def exec_func():
	'''���ƶ����ص��ļ����н�������ں�������Ҫ�������£�
	1����ѹ����
	2�����ÿ��Ŀ¼������Ӧ�Ľ����������н���
	'''
	global s_rootdir
	dir_list_info = {}
	dir_list_info = gfn.GetDirInfo(s_rootdir)
	#print dir_list_info
	for dir_key,dir_value in dir_list_info.items():
		try :
			parse_one_dir_file(dir_key,dir_list_info)
		except:
			log.error("func_name[exec_func]ִ�д���" )
			return False
	return True		

def exit_func():
	pass
	
def parse_entry():
	'''��ʼ����һ���ƶ��ϱ�������'''
	print 'hello,this is error'
	init_func()
	exec_func()
	exit_func()

def main():
	'''������ؽ������������'''
	single_process_run(parse_entry)

if __name__ == '__main__':
	main()