#!/usr/sbin/env python
#-*- coding:utf-8 -*-

import MySQLdb
import logProc as log
import sys

s_conn = ""
s_cursor = ""

def con_db():
	global s_conn
	global s_cursor
	try:           
		# 尝试连接数据库
		s_conn = MySQLdb.connect("localhost","root","root","FW_LOG_fwlog",charset="latin1")  # 定义连接数据库的信息
		s_cursor = s_conn.cursor()
		
	except :  # 连接失败提示
		log.error("dn connect error")
		sys.exit(1)
	
def sql_exec(sql_str):
	'执行数据库操作'
	global s_cursor
	try:
		s_cursor.execute(sql_str)  #使用cursor提供的方法来执行查询语句
	except:
		log.error("数据库插入失败")
		return False
	return True	
	
def sql_close():
	'关闭数据库操作'
	global s_cursor
	global s_conn
	try:
		s_cursor.close()            #关闭cursor对象
		s_conn.close()             #关闭数据库链接
	except:
		log.error("数据库不能正常关闭")
		sys.exit(1)

if __name__ == '__main__':
	con_db()
	str = "insert into QualityMonitorExecptionInfo(gataway_id,zombie_proc_info,execpt_reboot_info, core_dump_info,cpu_mem_info,core_proc_info,core_module_info,core_cfg_info,except_account_info,record_date) values('0DD3EB4A',1,1,0,1,1,0,0,0,'2016-09-02')"
	sql_exec(str)
	sql_close()
