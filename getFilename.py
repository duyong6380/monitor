#!/usr/sbin/env python
#coding:UTF-8

import os
import sys
import re
import logProc as log
import common

def GetDirFilename(FindPath):
	'��ȡ��Ҫ������Ŀ¼'
	dir_info = {}
	
	try :
		for dir in os.listdir(FindPath):
			for index in range(len(common.dir_key_info)):
				if re.search(common.dir_key_info[index] , dir) is not None :
					dir_info[common.dir_key_info[index]] = dir
	except:
		print '��ȡĿ¼ʧ��'
	return  dir_info
	
def GetFileListByDirName(key , dirname):
	'�����ض�Ŀ¼��ȡĿ¼�������ļ��ľ���·��'
	file_list = {}
	src_root_dir = []
	dst_root_dir = []
	
	try :
		for root,dirs,files in os.walk(dirname):
			for filespath in files:
				src_root_dir.append(root)
		dst_root_dir = list(set(src_root_dir))
	except:
		log.error("��ȡĿ¼ʧ��")
		return ""
	return dst_root_dir	  
	
def GetAllFileList(dir_dict,dir_path):
	'��һ��Ŀ¼�µ������ļ�����һ��Ԫ����'
	dir_file_info = {}
	for key,value in dir_dict.items():
		value = dir_path + value
		dir_file_info[key] = GetFileListByDirName(key , value)
	
	return dir_file_info

def GetDirInfo(rootdir):
	dir_info = {}
	dir_info = GetDirFilename(rootdir)
	return GetAllFileList(dir_info,rootdir)
	
if __name__ == '__main__':
	log.init_log()
	ROOTDIR = "/var/duyong/"
	GetDirInfo(ROOTDIR)
	 