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

# 用文件锁实现进程单例, 保证单例运行, 如果已经有进程调用还没退出，就会退出
# func          : 捕抓异常的操作
def single_process_run(func):
	'''捕抓文件锁异常，判断是否单进程'''
	global UPLOAD_PARSE_LOCK_FILE
	
	try:
		import fcntl
		f = open(UPLOAD_PARSE_LOCK_FILE, 'w')
		fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
	except Exception, e:
		f.close()
		func_name = func.__name__
		log.error('func_name:%s 已经存在一个实例在运行' %func_name)
		sys.exit(1)
	func() 
	fcntl.flock(f, fcntl.LOCK_UN)
	f.close()

def get_data_from_cloud():
	''' 从云端获取需要解析的数据,暂时不做'''
	pass
def check_db_table_create():
	''''''
	pass
	
def init_func():
	'''执行解析的初始化函数：主要功能如下：
	1、从云端自动获取当天需要解析的数据
	2、检查相应的数据库是否已经创建
	'''
	get_data_from_cloud()
	check_db_table_create()
	common.common_init()
	 	

def parse_one_dir_file(dir_key ,dir_list_info):
	'''解析一个目录下的文件'''
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
			log.error("解析失败[%s]" %(dir_key))
			sys.exit(1)
	return True
	
def exec_func():
	'''对云端下载的文件进行解析总入口函数，主要功能如下：
	1、解压数据
	2、针对每个目录调用相应的解析函数进行解析
	'''
	global s_rootdir
	dir_list_info = {}
	dir_list_info = gfn.GetDirInfo(s_rootdir)
	#print dir_list_info
	for dir_key,dir_value in dir_list_info.items():
		try :
			parse_one_dir_file(dir_key,dir_list_info)
		except:
			log.error("func_name[exec_func]执行错误" )
			return False
	return True		

def exit_func():
	pass
	
def parse_entry():
	'''开始解析一天云端上报的数据'''
	print 'hello,this is error'
	init_func()
	exec_func()
	exit_func()

def main():
	'''质量监控解析主函数入口'''
	single_process_run(parse_entry)

if __name__ == '__main__':
	main()