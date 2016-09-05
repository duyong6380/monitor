#!/usr/sbin/env python
#-*- coding:utf-8 -*-

import sqlProc as sql
import logProc as log
import time
import sys

s_debug_flag = 1

s_record_date = ""
s_dev_id = ""
s_base_info_sql = "insert into QualityMonitorBaseInfo (gataway_id,dev_name,hw_info,dev_ip,last_crash_time,days_run,upload_time,dev_platform,storage_platform,version,record_date,except_flag) values ("
s_sql_info = {}
s_sql_info['ZOMBIE'] = "insert into QualityMonitorZomBieInfo(gataway_id,zombie_proc,record_date) values"
s_sql_info['CORE_MODULE'] = "insert into QualityMonitorCoreModuleInfo(gataway_id,core_module_info,record_date) values"
s_sql_info['CORE_PROCESS'] = "insert into QualityMonitorCoreProcInfo(gataway_id,core_proc_info,record_date) values"
s_sql_info['CORE_CONF'] = "insert into QualityMonitorCoreConfInfo(gataway_id,core_conf_info,record_date) values"
s_sql_info['CPU'] = "insert into QualityMonitorCPUAndMemInfo(gataway_id , cpu_info, mem_info , record_date) values"
s_sql_info['STORAGE_CHECK'] = "insert into QualityMonitorStorageHardWareInfo(gataway_id ,content,record_date) values"
s_sql_info['OPENED_PORT'] = "insert into QualityMonitorOpenPortInfo(gataway_id ,port_info,record_date) values"
s_sql_info['DCLOG_SIZE'] = "insert into QualityMonitorLogInfo(gataway_id ,log_info,record_date) values"
s_sql_info['CORE_DUMP'] = "insert into QualityMonitorCoreProcInfo(gataway_id,core_dump_proc,record_date,core_dump_path) values"
s_sql_info['EXCEPT'] = "insert into QualityMonitorExecptionInfo(gataway_id,zombie_proc_info,execpt_reboot_info, core_dump_info,cpu_mem_info,core_proc_info,core_module_info,core_cfg_info,except_account_info,record_date) values"

def show_parse_data(data):
	global s_debug_flag 
	if s_debug_flag == 1:
		print data
	
def common_data_proc(dict,name):
	common_data = {}
	common_data = dict[name]
	common_data_len = len(common_data)
	if common_data_len == 0:
		print '不存在[%s]异常信息' %name
	return 	(common_data_len,common_data)

def strcat_sql(data,len):
	'''根据获取的数据进行拼接'''
	global s_dev_id
	common_data_info = ""
	
	for index  in range(1,len + 1 , 1):
		common_data_info += '(\'' \
					+ s_dev_id + '\', \''\
					+ data[index] + '\',\''\
					+ s_record_date + '\')'
		if index != len:
			common_data_info += ','
	return (True,common_data_info)		
	
def get_sql_values(dict,name):
	'''根据解析出来的值进行sql字符串的拼接''' 
	(common_data_len , common_data) = common_data_proc(dict,name)
	if common_data_len == 0 :
		return (False,"")
		
	show_parse_data(common_data)	
	return strcat_sql(common_data,common_data_len)

	
def exec_base_table_data(dict,flag):
	'对基本信息表进行数据插入'
	
	global s_base_info_sql
	base_info = {}
	(base_info_len,base_info) = common_data_proc(dict,'BASE')
	if base_info_len == 0 :
		return False
	sql_str = s_base_info_sql + '\'' + base_info['dev_id'] + '\',\''\
						  + base_info['customer'] + '\',\''\
						  + base_info['hard_plat'] + '\',\''\
						  + base_info['device_ip'] + '\',\''\
						  + base_info['crash_time'] + '\',\''\
						  + base_info['run_time'] + '\',\''\
						  + base_info['device_time'] + '\',\''\
						  + base_info['device_plat'] + '\',\''\
						  + base_info['storage_plat'] + '|'\
						  + dict['STORAGE_CHECK']['capacity'] + '\',\''\
						  + base_info['device_vervion'] +  '\',\''\
						  + s_record_date + '\',\''\
						  + str(flag) + '\')'				  
	sql.sql_exec(sql_str)
	return True
	

def get_last_insert_sql(name,common_sql_info):
	'''获取最后可以插入到数据库中的sql'''
	global s_sql_info
	sql_str = s_sql_info[name] + common_sql_info
	try :
		sql.sql_exec(sql_str)	
	except:
		log.error("name:[%s],common_sql_info:[%s]",name,common_sql_info)
		return False
	return True	
	
def common_proc_table_data(dict,name):
	(rtn , common_sql_info) = get_sql_values(dict,name)
	if rtn == False:
		return False
		
	show_parse_data(common_sql_info)
	return get_last_insert_sql(name,common_sql_info)	
		
def exec_zombie_table_data(dict):
	'对僵尸进程进行数据库写入'
	return common_proc_table_data(dict,'ZOMBIE')
	
def exec_core_dump_table_data(dict):
	'处理core_dump数据信息'
	return common_proc_table_data(dict,'CORE_DUMP')
	
def exec_core_module_table_data(dict):
	'处理核心模块信息'
	return common_proc_table_data(dict,'CORE_MODULE')

def exec_core_process_table_data(dict):
	'c处理核心进程信息'
	return common_proc_table_data(dict,'CORE_PROCESS')
	
def exec_core_conf_table_data(dict):
	'c处理核心配置文件信息'
	return common_proc_table_data(dict,'CORE_CONF')

def exec_cpu_and_mem_info(dict):
	'处理异常CPU或者是异常内存信息'
	global s_sql_info
	
	cpu_info = {}
	mem_info = {}
	sql_cpu_info = ""
	sql_mem_info = ""
	(cpu_rtn , cpu_info) = common_data_proc(dict,'CPU')
	(mem_rtn , mem_info) = common_data_proc(dict,'MEM')
	show_parse_data(mem_info)
	if cpu_rtn == True:
		sql_cpu_info = cpu_info['CPU']
	if mem_rtn == True:
		sql_mem_info  = mem_info['MEM']
	sql_str = s_sql_info['CPU'] + '(\''+ dict['BASE']['dev_id'] + '\',\'' \
									   + sql_cpu_info + '\',\'' \
									   + sql_mem_info + '\',\'' \
									   + s_record_date + '\')'
	try:
		sql.sql_exec(sql_str)
	except:
		log.error("异常CPU或者是MEM数据库处理失败")
		return False
	return True
	
def exec_storage_check_table_data(dict):
	'处理存储硬件异常'
	dict['STORAGE_CHECK'].pop('type')
	if 'capacity' in dict['STORAGE_CHECK'].keys():
		dict['STORAGE_CHECK'].pop('capacity')
	return common_proc_table_data(dict,'STORAGE_CHECK')

def exec_open_port_table_data(dict):
	'处理开放端口异常'
	return common_proc_table_data(dict,'OPENED_PORT')
	
def exec_dclog_table_data(dict):
	'处理异常内置数据中心日志'
	global s_record_date
	dclog_info = dict['DCLOG_SIZE']
	
	for key,value in dclog_info.items():
		str = key.split('_')
		s_record_date = str[1]
		(rtn , dclog_sql_info) = get_sql_values(dclog_info,key)
		if rtn == False:
			return False
		get_last_insert_sql('DCLOG_SIZE',dclog_sql_info)
	return True	
	
def createTableSql(info):
	''''''
	global s_dev_id
	global s_sql_info
	global s_record_date
	print s_dev_id
	s_except_sql = "('%s',%d,%d,%d,%d,%d,%d,%d,%d,'%s');" %(\
					s_dev_id,info['ZOMBIE'],info['EXCEPT_REBOOT'],\
					info['CORE_DUMP'],info['CORE_MODULE'],info['CORE_PROCESS'],\
					info['CPU'],info['CORE_CONF'],\
					info['ABNORMAL_USER'],s_record_date
					)

	
	s_except_sql = s_sql_info['EXCEPT'] + s_except_sql
	print s_except_sql
	
	sql.sql_exec(s_except_sql)
	
	return True
	
def exec_except_table_data(dict):
	'''将有问题的数据放进异常表'''
	except_info = {}
	for key,value in dict.items():
		if len(value) != 0:
			except_info[key] = 1
		else:
			except_info[key] = 0
	if len(dict['BASE']['crash_time']) == 0:
		except_info['EXCEPT_REBOOT'] = 0
	else:
		except_info['EXCEPT_REBOOT'] = 1
	
	if except_info['MEM'] == 1:
		except_info['CPU'] = 0
	print 	except_info	

	createTableSql(except_info)
	
	return True	
	
	
def sql_proc_entry(dict,except_flag):
		#dict
	print 'start to proc data tables '
	global s_dev_id 
	global s_record_date
	s_record_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	s_dev_id = dict['BASE']['dev_id']
	print s_dev_id

	exec_base_table_data(dict,except_flag)
	exec_except_table_data(dict)
	
	exec_zombie_table_data(dict)
	exec_core_dump_table_data(dict)
	exec_core_module_table_data(dict)
	exec_core_process_table_data(dict)
	exec_core_conf_table_data(dict)
	exec_cpu_and_mem_info(dict)
	exec_storage_check_table_data(dict)
	exec_open_port_table_data(dict)
	exec_dclog_table_data(dict)


if __name__ == '__main__':
	
	dict = {'CORE_MODULE': {1: 'sf_pcre no insmod', 2: 'led no insmod', 3: 'exclude no insmod', 4: 'bypass no insmod', 5: 'watchdog no insmod', 6: 'dosck_drv no insmod'}, 'CORE_PROCESS': {1: 'fluxctrld no exists', 2: 'smssp no exists', 3: 'sms_proxy no exists'}, 'MEM': {}, 'CORE_CONF': {}, 'ZOMBIE': {1: 'cron.sh', 2: 'cleancore.sh', 3: 'timesync.sh', 4: 'sec_event_check', 5: 'uploadReport.sh'}, 'BASE': {'customer': 'Default authorized user', 'dev_id': '0DD3EB4A', 'device_vervion': 'AF7.0.132 EN Build20160816', 'device_time': '20160820 05:00:02', 'device_plat': '4G2C', 'device_ip': '111.111.112.216', 'hard_plat': 'UNKNOWN', 'crash_time': 'Crashed time:2012-02-14 23:48:41', 'run_time': '0 days', 'storage_plat': 'DISK'}, 'STORAGE_CHECK': {1: 'tmpfs /fwlog/ads/redir_cache tmpfs rw,relatime,size=30720k 0 0', 2: 'tmpfs /var/tmp/kvfilter tmpfs rw,relatime,size=102400k 0 0', 3: 'rootfs / rootfs rw 0 0', 4: '/proc /proc proc rw,relatime 0 0', 5: 'tmpfs /var/run tmpfs rw,relatime,size=2048k 0 0', 6: 'tmpfs /var/tmp/darkchain tmpfs rw,relatime,size=20480k 0 0', 7: 'tmpfs /fwlog/ip_sess_count/often_write tmpfs rw,relatime,size=2048k 0 0', 8: '/dev/sda1 /boot ext3 rw,noatime,errors=continue,data=ordered 0 0', 9: '/dev/sys /sys sysfs rw,relatime 0 0', 10: 'tmpfs /var/often_write tmpfs rw,relatime,size=4096k 0 0', 11: 'shm /dev/shm tmpfs rw,nosuid,nodev,relatime 0 0', 12: 'tmpfs /fwlog/log_data/tmp tmpfs rw,relatime,size=20480k 0 0', 13: '/dev/sda6 /fwlog ext3 rw,noatime,errors=continue,data=ordered 0 0', 14: '/dev/root / ext3 rw,relatime,errors=continue,data=journal 0 0', 15: 'none /dev/pts devpts rw,relatime,gid=5,mode=620 0 0', 16: '/dev/sda3 /fwlib ext3 rw,noatime,errors=continue,data=ordered 0 0', 17: 'tmpfs /fwlog/ads/spider/rtinfo tmpfs rw,relatime,size=2048k 0 0', 18: 'tmpfs /var/often_read tmpfs rw,relatime,size=4096k 0 0', 'capacity': '7', 'type': 'DISK'}, 'OPENED_PORT': {1: 'udp,0,0,0.0.0.0:51111,0.0.0.0:*,', 2: 'tcp,0,0,0.0.0.0:54322,0.0.0.0:*,LISTEN', 3: 'udp,0,0,0.0.0.0:40059,0.0.0.0:*,', 4: 'tcp,0,0,0.0.0.0:850,0.0.0.0:*,LISTEN', 5: 'tcp,0,0,131.166.111.219:9000,131.166.111.218:13830,TIME_WAIT', 6: 'tcp,0,0,0.0.0.0:9000,0.0.0.0:*,LISTEN', 7: 'udp,0,0,0.0.0.0:1813,0.0.0.0:*,', 8: 'tcp,0,0,0.0.0.0:800,0.0.0.0:*,LISTEN', 9: 'tcp,0,0,0.0.0.0:80,0.0.0.0:*,LISTEN', 10: 'raw,90400,0,0.0.0.0:112,0.0.0.0:*,112', 11: 'tcp,0,0,0.0.0.0:8000,0.0.0.0:*,LISTEN', 12: 'tcp,0,0,131.166.111.219:9000,131.166.111.218:13832,TIME_WAIT', 13: 'udp,0,0,0.0.0.0:36146,0.0.0.0:*,', 14: 'tcp,0,0,0.0.0.0:22345,0.0.0.0:*,LISTEN', 15: 'raw,0,0,0.0.0.0:112,0.0.0.0:*,112', 16: 'tcp,0,0,0.0.0.0:443,0.0.0.0:*,LISTEN', 17: 'udp,0,0,0.0.0.0:58983,0.0.0.0:*,', 18: 'tcp,0,0,0.0.0.0:54321,0.0.0.0:*,LISTEN', 19: 'udp,0,0,0.0.0.0:32837,0.0.0.0:*,', 20: 'udp,0,0,0.0.0.0:41485,0.0.0.0:*,', 21: 'tcp,0,0,0.0.0.0:851,0.0.0.0:*,LISTEN', 22: 'udp,0,0,0.0.0.0:51441,0.0.0.0:*,', 23: 'udp,0,0,0.0.0.0:58842,0.0.0.0:*,', 24: 'tcp,0,0,0.0.0.0:51111,0.0.0.0:*,LISTEN', 25: 'udp,0,0,0.0.0.0:1980,0.0.0.0:*,', 26: 'udp,0,0,0.0.0.0:55449,0.0.0.0:*,', 27: 'tcp,0,0,0.0.0.0:85,0.0.0.0:*,LISTEN', 28: 'tcp,0,0,0.0.0.0:65534,0.0.0.0:*,LISTEN', 29: 'tcp,0,0,0.0.0.0:442,0.0.0.0:*,LISTEN', 30: 'tcp,0,0,0.0.0.0:81,0.0.0.0:*,LISTEN', 31: 'tcp,0,0,0.0.0.0:4420,0.0.0.0:*,LISTEN', 32: 'tcp,0,0,131.166.111.219:9000,131.166.111.218:13833,TIME_WAIT', 33: 'tcp,0,0,131.166.111.219:9000,131.166.111.218:13831,TIME_WAIT', 34: 'tcp,0,0,0.0.0.0:8001,0.0.0.0:*,LISTEN', 35: 'udp,0,0,100.100.89.219:43424,8.8.8.8:53,ESTABLISHED'}, 'DCLOG_SIZE': {'DCLOG_20160815': {1: '/fwlog/log_data/fwlog/20160815/frm,160.0K', 2: '/fwlog/log_data/fwlog/20160815/read_status,4.0K', 3: '/fwlog/log_data/fwlog/20160815,168.0K'}, 'DCLOG_20160816': {1: '/fwlog/log_data/fwlog/20160816/frm,160.0K', 2: '/fwlog/log_data/fwlog/20160816/read_status,12.0K', 3: '/fwlog/log_data/fwlog/20160816,208.0K', 4: '/fwlog/log_data/fwlog/20160816/T,32.0K'}, 'DCLOG_20160817': {1: '/fwlog/log_data/fwlog/20160817/frm,160.0K', 2: '/fwlog/log_data/fwlog/20160817/read_status,4.0K', 3: '/fwlog/log_data/fwlog/20160817,168.0K'}, 'DCLOG_20160820': {1: '/fwlog/log_data/fwlog/20160820/frm,160.0K', 2: '/fwlog/log_data/fwlog/20160820/read_status,4.0K', 3: '/fwlog/log_data/fwlog/20160820,168.0K'}, 'DCLOG_20160818': {}, 'DCLOG_20160819': {}}, 'CORE_DUMP': {}, 'CPU': {}, 'ABNORMAL_USER': {}}
	#exec_except_table_data(dict)
	sql_proc_entry(dict,1)
								