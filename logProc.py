#!/usr/sbin/env python
#coding:UTF-8
import logging

def init_log():
	'日志记录窗口'
	log_format = '%(filename)s,lineno:%(lineno)d [%(asctime)s] %(message)s'
	logging.basicConfig(format = log_format,datefmt='%Y-%m-%d %H:%M:%S %p',\
						filename='/var/log/uploadParsefile_log')


def del_log():	
	pass				

def error(str):
	return logging.error(str)	
def info(str):
	return logging.info(str)
