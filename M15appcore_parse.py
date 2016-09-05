#!/usr/sbin/env python
#-*- coding:utf-8 -*-

import common
import os

s_key_value = 'M15appcore'

def run(dirpath, file):

	root_path = common.createDirByKey(file , s_key_value)
	
	filelist = os.listdir(dirpath)
	for zipfile in filelist:
		cmd = "unzip -jxo " + dirpath + '/' +zipfile + ' -d ' + root_path
		print 'cmd :',cmd
		rtn = os.system(cmd)
		if rtn == 0 :
			filename = dirpath + '/' +zipfile
			os.remove(filename)	
	return True
	
def init_func():
	pass