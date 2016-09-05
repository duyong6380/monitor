#!/usr/sbin/env python
#-*- coding:utf-8 -*-

import common

s_key_value = 'M05applog'
s_module_filename = 'app_log.log'


def run(dirname , file):
	global s_key_value
	global s_module_filename
	return common.common_proc(dirname , file ,s_key_value , s_module_filename )


def init_func():
	pass