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
		# �����������ݿ�
		s_conn = MySQLdb.connect("localhost","root","root","FW_LOG_fwlog",charset="latin1")  # �����������ݿ����Ϣ
		s_cursor = s_conn.cursor()
		
	except :  # ����ʧ����ʾ
		log.error("dn connect error")
		sys.exit(1)
	
def sql_exec(sql_str):
	'ִ�����ݿ����'
	global s_cursor
	try:
		s_cursor.execute(sql_str)  #ʹ��cursor�ṩ�ķ�����ִ�в�ѯ���
	except:
		log.error("���ݿ����ʧ��")
		return False
	return True	
	
def sql_close():
	'�ر����ݿ����'
	global s_cursor
	global s_conn
	try:
		s_cursor.close()            #�ر�cursor����
		s_conn.close()             #�ر����ݿ�����
	except:
		log.error("���ݿⲻ�������ر�")
		sys.exit(1)

if __name__ == '__main__':
	con_db()
	str = "insert into QualityMonitorExecptionInfo(gataway_id,zombie_proc_info,execpt_reboot_info, core_dump_info,cpu_mem_info,core_proc_info,core_module_info,core_cfg_info,except_account_info,record_date) values('0DD3EB4A',1,1,0,1,1,0,0,0,'2016-09-02')"
	sql_exec(str)
	sql_close()
