#!/usr/sbin/env python
#-*- coding:utf-8 -*-

import os 
import re
import sys
import logProc as log

def write_to_file(dst_file,src_file,dirname):
	dst_file = dirname + '/' + dst_file	+ '_temp'
	src_file = dirname + '/' + src_file
	
	if os.path.exists(src_file) == False or dst_file == src_file:
		return ""
	
	try:		
		src_f = open(src_file,'r+')
		dst_f = open(dst_file , "a+")
		for eachline in src_f:
			dst_f.write(eachline)
	except IOError as e:	
		log.error("open file failed ")
	src_f.close()
	dst_f.close()	
	return os.path.basename(dst_file)

def getSplitNum(strs):
	'''
	返回值：
	1、结束
	2、不结束
	'''
	file_index = strs[4].split('.')
	if int(file_index[0]) > int(strs[3]):
		return 0
	return file_index[0]

def getMergeFileName(file_dict,dirname):
	file_list = []
	filename_tmp = ""
	for key,value in file_dict.items():
		length = len(value)
		for index in range(1,len(value)+1 , 1):
			strs = value[str(index)].split('_')
			if int(strs[3]) != length:
				break
			#print 'filename:',value[str(index)]
			filename_tmp = write_to_file(strs[0],value[str(index)] ,dirname)
		
		if filename_tmp != "":
			file_list.append(filename_tmp)
	return 	file_list
	
def updateDictFileList(strs, filename,dict_file):	
	new_dict_info = {}
	index = getSplitNum(strs)
	if len(dict_file) == 0:
		new_dict_info[index] = filename
		return new_dict_info
		
	#print 'dict_file:',dict_file
	
	if strs[0] not in dict_file.keys():
		dict_file[strs[0]] = {}
	new_dict_info = dict_file[strs[0]]
	
	
	new_dict_info[index] = filename
	return new_dict_info
		

def merge_mutil_file_to_one(dirname ,list_dir_file):
	'''
	 对于多重切分文件进行合并
	'''
	new_file_list = []
	mutil_file_list = {}
	filename_list = []
	for filename in list_dir_file:
		#print 'filename:',filename
		strs = filename.split('_')
		if len(strs) != 7:
			continue
		
		if strs[3] == '1':
			new_file_list.append(filename)
			continue
		'''根据时间戳和切分块来进行字典排列，必须保证是顺序索引进行排列的'''
		#print 'file_list:',mutil_file_list
		mutil_file_list[strs[0]] = updateDictFileList(strs , filename,mutil_file_list)
		
		
	filename_list = getMergeFileName(mutil_file_list,dirname)
	
	if len(filename_list) == 0:
		return new_file_list
		
	for filelist in filename_list:
		new_file_list.append(filelist)
	return 	new_file_list

if __name__ == "__main__":
	dirname = "/var/duyong/M05applog_7.0/4E/32/4E32903A"
	list_info = ['1471716006_M05applog_7.0_1_1.470179840_1000_NjcyNA==', '1471629605_M05applog_7.0_1_1.470179840_1000_NDg2', '1472061606_M05applog_7.0_1_1.470179840_1000_MTM0', '1471975206_M05applog_7.0_1_1.470179840_1000_Mjg4MA==', '1472234406_M05applog_7.0_1_1.470179840_1000_NDg3Nw==', '1471888805_M05applog_7.0_1_1.470179840_1000_NjkzMQ==', '1471543205_M05applog_7.0_1_1.470179840_1000_MzA1Nw==', '1472407205_M05applog_7.0_2_2.470179840_1000_OTkzOQ==', '1471284011_M05applog_7.0_1_1.470179840_1000_NTgxNw==', '1472493606_M05applog_7.0_2_1.470179840_1000_NzgwMA==', '1472148005_M05applog_7.0_1_1.470179840_1000_MjgyOA==', '1472320806_M05applog_7.0_2_1.470179840_1000_NTAwMw==', '1471370404_M05applog_7.0_1_1.470179840_1000_MzQyNw==', '1472320806_M05applog_7.0_2_2.470179840_1000_ODc1Ng==', '1472493606_M05applog_7.0_2_2.470179840_1000_MzcxNA==', '1472407205_M05applog_7.0_2_1.470179840_1000_ODk1Nw==', '1471802406_M05applog_7.0_1_1.470179840_1000_Mzk3NQ==', '1471456805_M05applog_7.0_1_1.470179840_1000_NjUw']
	new_list = []
	new_list = merge_mutil_file_to_one(dirname,list_info)
	print '=================================='
	print 'mew_list :',new_list
	print '==================================='