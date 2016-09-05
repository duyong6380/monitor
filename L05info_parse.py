#!/usr/sbin/env python
#-*- coding:utf-8 -*-

import sys
import ConfigParser
import re
import logProc as log
import sqlProc as sql
import dbDataProc as dbd

s_module_filename = 'sys_info.txt'

def parse_base_info(cf,name):
	'开始解析base类信息'
	base_info = {}
	try :
		base_info['dev_id'] = cf.get(name,"dev_id")
		base_info['customer'] = cf.get(name,"customer")
		base_info['hard_plat'] = cf.get(name,"hard_plat")
		base_info['device_ip'] = cf.get(name,"device_ip")
		base_info['crash_time'] = cf.get(name,"crash_time")
		base_info['run_time'] = cf.get(name,"run_time")
		base_info['device_time'] = cf.get(name,"device_time")
		base_info['device_plat'] = cf.get(name,"device_plat")
		base_info['storage_plat'] = cf.get(name,"storage_plat")
		base_info['device_vervion'] = cf.get(name,"device_vervion")
	except:
		log.error('解析文件存在问题')
		base_info = {}
	return base_info

def get_section_cnt(cf,name):
	'获取每个段下面key的个数'
	try:
		cnt = cf.get(name,"cnt")
	except:
		log.error("section:[%s] 不存在子健")
		return 0
	return int(cnt)	
		
def common_parse_func(cf,name):
	'通用解析函数'
	common_st = {}
	src_list_st = []
	dst_list_st = []
	cnt = get_section_cnt(cf,name)

	if cnt == 0 :
		return common_st

	try:
		''' 对元素进行去重操作，执行使用列表形式'''
		for index in range(1,cnt+1,1):
			tmp_list = cf.get(name,str(index))
			src_list_st.append(tmp_list)
		
		dst_list_st = list(set(src_list_st))
		dst_len = len(dst_list_st)
		
		log.info("name:%s,dst_list_st:%s , len:%d" %(name,dst_list_st,dst_len))
		
		''' 将列表元素转换成字典，这样可以进行映射'''
		for i in range(dst_len):
			index = i + 1
			common_st[index] = dst_list_st[i]
	except:
		log.error("通用解析函数存在问题，当前段是[%s],cnt[%d]" %(name,cnt))
		common_st = {}
	return common_st
		
def proc_DCLOG_SIZE_info(cf,name):
	'开始处理内置数据中心日志'
	dclog_size_info = {}
	cnt = int(cf.get(name,"cnt"))
	if cnt == 0:
		return ""
	for i in range(1,cnt,1):
		key_word = "DCLOG_DATE" + str(i)
		print 'key_word',key_word
		dclog_size_key =cf.get(name,key_word)
		key_word = "DCLOG_" + dclog_size_key
		dclog_size_info[key_word] = common_parse_func(cf,key_word)
		
	return 	dclog_size_info

def proc_SPEC_SECTION_info(cf,name):
	'特殊段进行特殊处理'
	spec_section_info = {}
	print '这是特殊区段，后续进行特殊处理'
	return spec_section_info

def proc_CPU_and_MEM_info(cf,name):
	'处理cpu 和 内存的信息'
	cpu_and_mem_info = {}
	tmp_name = name.lower()
	key_value = tmp_name + "_usage"
	try:
		key_value = cf.get(name,key_value)
		if key_value != "Normal":
			cpu_and_mem_info[name] = key_value
	except:
		log.error("获取CPU信息时错误")
		cpu_and_mem_info = {}
	return cpu_and_mem_info

def proc_STORAGE_CHECK_info(cf,name):
	'处理存储硬件信息'
	storage_check_info = {}
	type = cf.get(name,'type')
	try:
		storage_check_info = common_parse_func(cf,name)
		if type == 'SSD':
			storage_check_info['capacity'] = cf.get(name,'capacity')
		else :
			storage_check_info['capacity'] = cf.get(name,'heal_status')
	except:
		log.error("存储硬件信息获取去出现错误,类型是:",type)
	
	storage_check_info['type'] = type
	print storage_check_info	
	return storage_check_info
	
def del_DCLOG_day_sec(section):
	'删除内置数据中天段，提到DCLOG_SIZE段进行解析'
	new_section = []
	try:
		for name in section:
			m = re.search('DCLOG_2',name)
			if m is None:
				new_section.append(name)
	except:
		log.error("删除冗余段出现错误，当前删除段名为:",name)
		new_section = []
	return new_section
	
def proc_SMART_CTL_info (cf,name):
	key = cf.get(name,'key')
	print 'key:',key
	sys.exit(1)
	
def init_parse_func():
	##创建回调函数
	cb = {}
	cb['BASE'] = parse_base_info
	cb['DCLOG_SIZE'] = proc_DCLOG_SIZE_info
	cb['CPU'] = proc_CPU_and_MEM_info
	cb['MEM'] = proc_CPU_and_MEM_info
	cb['STORAGE_CHECK'] = proc_STORAGE_CHECK_info
	cb['SMARTCTL'] = proc_SPEC_SECTION_info
	cb['ABNORMAL_USER'] = proc_SPEC_SECTION_info
	cb['ZOMBIE'] = common_parse_func
	cb['CORE_CONF'] = common_parse_func
	cb['CORE_PROCESS'] = common_parse_func
	cb['OPENED_PORT'] = common_parse_func
	cb['CORE_DUMP'] = common_parse_func
	cb['CORE_MODULE'] = common_parse_func
	return cb

def get_cfg_handle(filename):
	'根据文件名获取配置处理句柄'
	need_parse_file = filename
	cf = ConfigParser.ConfigParser()
	cf.read(need_parse_file)
	return cf

def get_sections(cf):
	'根据句柄获取文件中的区段'
	section = cf.sections()
	section = del_DCLOG_day_sec(section)
	return section
	
def exec_callback(section,cb,cf):
	#返回的字典对象
	result_dict = {}
	try:
		for name in section:  
			result_dict[name] = cb[name](cf,name)
	except:
		log.error("可能回调函数不存在，或者是段[%s]不存在" %name)
		result_dict = {}
	return result_dict
	
def get_except_flag_by_data(dict):
	'''
	'根据已经解析出来的数据判断当前设备是否出现异常'
	判断逻辑：1、是否存在宕机时间
			  2、是否存在僵尸进程
			  3、是否存在core_dump
			  4、是否存在CPU或者是内存异常
			  5、是否存在核心进程、核心模块、核心配置文件异常
			  6、是否存在异常用户异常
	'''
	except_var = ['ZOMBIE','CORE_DUMP','CORE_CONF','CORE_MODULE','CORE_PROCESS','CPU','MEM']
	if dict['BASE']['crash_time'] is not None :
		return 1
	for i in range(len(except_var)):
		if len(dict[expect[i]]) != 0 :
			return 1
	return 0

def run(driname,tmp_file):
	#全局回调函数
	global s_module_filename
	file = driname + '/'+s_module_filename
	print 'file:',file
	print '*****************************************************'
	
	cb = {}
	cb = init_parse_func()
	try:
		cf = get_cfg_handle(file)
		section = get_sections(cf)
		print 'section:',section

		new_dict = {}
		new_dict = exec_callback(section,cb,cf)
		
		print 'core_process:',new_dict['CORE_PROCESS']
		print '===========================数据已经解析完成，下面进行判断是插入数据库==================='
		flag = get_except_flag_by_data(new_dict)
		print flag
		dbd.sql_proc_entry(new_dict , flag)
		os.remove(file)
	except:
		log.error("L05info出现问题")
		sys.exit(1)
		
def init_func():
	sql.con_db()
	log.init_log()
	
if __name__ == '__main__':
	init_func()
	file = 'sys_info.txt'
	dirname = '/tmp/after/L05info/'
	run(dirname , file)


	