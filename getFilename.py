#!/usr/sbin/env python
#coding:UTF-8

import os
import sys
import re
import logProc as log
import common

def GetDirFilename(FindPath):
	'获取需要解析的目录'
	dir_info = {}
	
	try :
		for dir in os.listdir(FindPath):
			for index in range(len(common.dir_key_info)):
				if re.search(common.dir_key_info[index] , dir) is not None :
					dir_info[common.dir_key_info[index]] = dir
	except:
		print '获取目录失败'
	return  dir_info
	
def GetFileListByDirName(key , dirname):
	'根据特定目录获取目录下所有文件的绝对路径'
	file_list = {}
	src_root_dir = []
	dst_root_dir = []
	
	try :
		for root,dirs,files in os.walk(dirname):
			for filespath in files:
				src_root_dir.append(root)
		dst_root_dir = list(set(src_root_dir))
	except:
		log.error("获取目录失败")
		return ""
	return dst_root_dir	  
	
def GetAllFileList(dir_dict,dir_path):
	'将一个目录下的所有文件放在一个元祖中'
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
	 