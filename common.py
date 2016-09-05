#!/usr/sbin/env python
#coding:UTF-8

'''
本脚本的功能：
1、解压文件
2、执行回调
'''
import L05info_parse
import M10crashlog_parse
import L10userwebopr_parse
import M05applog_parse
import M15appcore_parse
import logging as log 
import os 
import tarfile
import time

s_unzip_save_dir = '/tmp/after/'

s_upload_storage_rootdir = '/var/log_data/appcore/'

dir_key_info = ['L05info','M10crashlog','L10userwebopr','M05applog','M15appcore']
parse_cb = {}

def delTempFile(filelist):
	''' 删除临时存储的文件'''
	for filename in filelist:
		tmp_name = os.path.basename(filename)
		strs = tmp_name.split('_')
		if len(strs) == 2 and strs[1] == 'temp': 
			os.remove(filename)
	return True		


def common_proc(dirname , file , s_key_value , s_module_filename):
	root_path = createDirByKey(file , s_key_value )
	if root_path == "" :
		return False
		
	cmd = 'cp -rf ' + dirname + '/' + s_module_filename + ' ' + root_path
	
	#print 'cmd :',cmd
	rtn = os.system(cmd)
	if rtn == 0:
		filename = dirname + '/' + s_module_filename
		os.remove(filename)
	return True
	
def construct_unrar_cmd(filename,dir,num):
	cmd = "tar xvf " + filename + " --strip-components " +  str(num) + " -C " + dir + " >>/dev/null"
	return cmd
	
def uncompress(key,file_path):
	global s_unzip_save_dir
	try:
		tmp_unzip_save_dir = s_unzip_save_dir + key
		if os.path.exists(tmp_unzip_save_dir) == False:
			os.makedirs(tmp_unzip_save_dir)
			
		num = 3
		if key == 'L10userwebopr':
			num = 2
		cmd = construct_unrar_cmd(file_path,tmp_unzip_save_dir,num)
		rtn = os.system(cmd)
		if rtn != 0 :
			return ""
	except Exception as e:
		log.info('unzip file:' + file_path)
		log.warning(e)
		return ""  
	return tmp_unzip_save_dir	

def common_parse_hook(filelist , key):
	'''根据键值来回调对应的钩子函数'''
	#print 'key:',key
	global parse_cb
	for file in filelist:
		print 'common:',file
		parse_dir = uncompress(key , file)
		if parse_dir == "":
			return False
		print 'parse_dir:',parse_dir
		cb_func_name = parse_cb[key] + '.run'
		try :
			eval(cb_func_name)(parse_dir , file)	
		except:
			log.error("模块[%s]解析失败" %parse_cb[key])
			return False
	return True

def getDevIdByPath(file):
	if file == "":
		return ""

	dev = os.path.dirname(file)
	if dev == "":
		return ""
	dev = os.path.basename(dev)
	if dir == "":
		return ""
	return dev	
	
def createDirByKey(file , key):
	global s_upload_storage_rootdir
	if key == "":
		return ""
	dev_id = getDevIdByPath(file)
	if dev_id == "":
		return ""

	time_str = time.strftime('%Y%m%d',time.localtime(time.time()))
	root_dir = s_upload_storage_rootdir + key + '/' + time_str + '/' + dev_id
	
	if os.path.exists(root_dir) == False:
		os.makedirs(root_dir)
	return root_dir	
		

def common_init():
	global parse_cb
	for index in range(len(dir_key_info)):
		parse_cb[dir_key_info[index]] = dir_key_info[index] + '_parse'
		print parse_cb[dir_key_info[index]]
		cb_func_name = parse_cb[dir_key_info[index]] + '.init_func'
		eval(cb_func_name)()
		
if __name__ == '__main__':
	filelist = ['/var/duyong/L05info_7.0/4E/32/4E32903A/1471370403_L05info_7.0_1_1.470179840_1000_NjkwNA==', '/var/duyong/L05info_7.0/4E/32/4E32903A/1472061606_L05info_7.0_1_1.470179840_1000_NDQ1NA==', '/var/duyong/L05info_7.0/4E/32/4E32903A/1471975205_L05info_7.0_1_1.470179840_1000_NDgxMw==', '/var/duyong/L05info_7.0/4E/32/4E32903A/1472493606_L05info_7.0_1_1.470179840_1000_MzgzNw==', '/var/duyong/L05info_7.0/4E/32/4E32903A/1472320805_L05info_7.0_1_1.470179840_1000_MjcyNg==', '/var/duyong/L05info_7.0/4E/32/4E32903A/1471543205_L05info_7.0_1_1.470179840_1000_MzA3OA==', '/var/duyong/L05info_7.0/4E/32/4E32903A/1471629605_L05info_7.0_1_1.470179840_1000_MjM5NA==', '/var/duyong/L05info_7.0/4E/32/4E32903A/1472407205_L05info_7.0_1_1.470179840_1000_NDE5MA==', '/var/duyong/L05info_7.0/4E/32/4E32903A/1471716005_L05info_7.0_1_1.470179840_1000_NDQzNQ==', '/var/duyong/L05info_7.0/4E/32/4E32903A/1472234405_L05info_7.0_1_1.470179840_1000_OTQ1NQ==', '/var/duyong/L05info_7.0/4E/32/4E32903A/1472148005_L05info_7.0_1_1.470179840_1000_NTkxNg==', '/var/duyong/L05info_7.0/4E/32/4E32903A/1471284011_L05info_7.0_1_1.470179840_1000_NzM4MQ==', '/var/duyong/L05info_7.0/4E/32/4E32903A/1471888805_L05info_7.0_1_1.470179840_1000_NDQy', '/var/duyong/L05info_7.0/4E/32/4E32903A/1471456805_L05info_7.0_1_1.470179840_1000_MzA4NQ==', '/var/duyong/L05info_7.0/4E/32/4E32903A/1471802406_L05info_7.0_1_1.470179840_1000_NDIzMQ==']
	key = 'L05info'
	common_init()
	common_parse_hook(filelist,key)
	