#!/usr/sbin/env python
#-*- coding:utf-8 -*-

import sys
import ConfigParser
import re
import logProc as log
import sqlProc as sql
import dbDataProc as dbd
import stateException as ex
import os

s_module_filename = 'sys_info.txt'

class L05infoParse(object):
    ''''''
    def __init__(self):
        self.module_file = 'sys_info.txt'
        self.init_func()
        self.cb = self.init_parse_func()
    def init_func(self):
        sql.con_db()
        log.init_log()
    def run(self,dirname):
        '''运行时函数，直接跑逻辑'''
        file = dirname + self.module_file
        dict_info = {}
        dict_info = self.get_dict_by_cfg(file)

        print 'dict......',dict_info

        print '================获取数据已经成功====================='
        if not dict_info :
            return True
        try:
            self.insert_data_to_db(dict_info)
        except :    
            print '配置文件插入数据数据失败'
            return False
        return True

    def insert_data_to_db(self , dict_info):
        ''' 将字典信息插入到数据库中'''
        assert dict_info != ""

        flag = self.get_except_flag_from_dict(dict_info)
        try:
            dbd.sql_proc_entry(dict_info , flag)
        except:
            return False
        return True

    def get_dict_by_cfg(self, file):
        '''根据配置文件获取数据，并将数据填充进字典中'''
        print 'file:',file
        cf = self.get_cfg_handle(file)
        section = self.get_sections(cf)
        new_dict = {}
        new_dict = self.exec_callback(section,cf)
        return new_dict

    def parse_base_info(self,cf,name):
        '开始解析base类信息'
        base_info = {}
        base_key = ['dev_id','customer','hard_plat','device_ip','crash_time',\
                    'run_time','device_time','device_plat','storage_plat','device_version']
        key_len = len(base_key)            
        for index in range(key_len): 
            try:
                base_info[base_key[index]] = cf.get(name,base_key[index])
            except:
                base_info[base_key[index]] = ""
        return base_info

    def get_section_cnt(self,cf,name):
        '获取每个段下面key的个数'
        try:
            cnt = cf.get(name,"cnt")
        except:
            print 'section:[%s] 不存在子健' %name
            return 0
        return int(cnt)	
            
    def common_parse_func(self,cf,name):
        '通用解析函数'
        common_st = {}
        src_list_st = []
        dst_list_st = []
        cnt = self.get_section_cnt(cf,name)

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
            
    def proc_DCLOG_SIZE_info(self,cf,name):
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
            dclog_size_info[key_word] = self.common_parse_func(cf,key_word)
            
        return 	dclog_size_info

    def proc_SPEC_SECTION_info(self,cf,name):
        '特殊段进行特殊处理'
        spec_section_info = {}
        print '这是特殊区段，后续进行特殊处理'
        return spec_section_info

    def proc_CPU_and_MEM_info(self , cf,name):
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

    def proc_STORAGE_CHECK_info(self ,cf,name):
        '处理存储硬件信息'
        storage_check_info = {}
        type = cf.get(name,'type')
        try:
            storage_check_info = self.common_parse_func(cf,name)
            if type == 'SSD':
                storage_check_info['capacity'] = cf.get(name,'capacity')
            else :
                storage_check_info['capacity'] = cf.get(name,'heal_status')
        except:
            log.error("存储硬件信息获取去出现错误,类型是:",type)
        
        storage_check_info['type'] = type
        print storage_check_info	
        return storage_check_info
        
    def del_DCLOG_day_sec(self ,section):
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
        
    def proc_SMART_CTL_info (self ,cf,name):
        key = cf.get(name,'key')
        print 'key:',key
        return ""
        
    def init_parse_func(self):
        ##创建回调函数
        cb = {}
        cb['BASE'] = self.parse_base_info
        cb['DCLOG_SIZE'] = self.proc_DCLOG_SIZE_info
        cb['CPU'] = self.proc_CPU_and_MEM_info
        cb['MEM'] = self.proc_CPU_and_MEM_info
        cb['STORAGE_CHECK'] = self.proc_STORAGE_CHECK_info
        cb['SMARTCTL'] = self.proc_SPEC_SECTION_info
        cb['ABNORMAL_USER'] = self.proc_SPEC_SECTION_info
        cb['ZOMBIE'] = self.common_parse_func
        cb['CORE_CONF'] = self.common_parse_func
        cb['CORE_PROCESS'] = self.common_parse_func
        cb['OPENED_PORT'] = self.common_parse_func
        cb['CORE_DUMP'] = self.common_parse_func
        cb['CORE_MODULE'] = self.common_parse_func
        return cb

    def get_cfg_handle(self ,filename):
        '根据文件名获取配置处理句柄'
        need_parse_file = filename
        cf = ConfigParser.ConfigParser()
        cf.read(need_parse_file)
        return cf

    def get_sections(self ,cf):
        '根据句柄获取文件中的区段'
        section = cf.sections()
        section = self.del_DCLOG_day_sec(section)
        return section
        
    def exec_callback(self,section,cf):
        #返回的字典对象

        assert section != ""
        result_dict = {}
        for name in section:  
            try:
                result_dict[name] = self.cb[name](cf,name)
                print 'section:%s 获取数据成功' %name
            except:
                print '可能回调函数不存在，或者是段[%s]不存在' %name
                result_dict[name] = {}
                
        return result_dict
        
    def get_except_flag_from_dict(self ,dict):
        '''
        '根据已经解析出来的数据判断当前设备是否出现异常'
        判断逻辑：1、是否存在宕机时间
                  2、是否存在僵尸进程
                  3、是否存在core_dump
                  4、是否存在CPU或者是内存异常
                  5、是否存在核心进程、核心模块、核心配置文件异常
                  6、是否存在异常用户异常
        返回值： 1表示存在异常，0表示正常         
        '''
        if dict == "":
            return 0
        except_var = ['ZOMBIE','CORE_DUMP','CORE_CONF','CORE_MODULE','CORE_PROCESS','CPU','MEM']
        if dict['BASE']['crash_time'] != "":
            return 1
        for i in range(len(except_var)):
            if len(dict[expect[i]]) != 0 :
                return 1
        return 0

if __name__ == '__main__':
    parse_class = L05infoParse()
    print 'hello,world'
    dirname = '/tmp/after/L05info/'
    parse_class.run(dirname)


	
