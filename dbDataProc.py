#!/usr/sbin/env python
#-*- coding:utf-8 -*-

import sqlProc as sql
import logProc as log
#import time
import sys
import datetime

class DbDataOpr(object):
    def __init__(self):
        self.dev_id = ""
        self.record_date = ""
        self.debug_flag = 0
        self.sql_info = self.init_sql_arr()
    def init_sql_arr(self):
        s_sql_info = {}
        s_sql_info['BASE'] = "insert into QualityMonitorBaseInfo (gataway_id,\
                           dev_name,hw_info,dev_ip,last_crash_time,days_run,\
                           upload_time,dev_platform,storage_platform,version,\
                           record_date,except_flag) values ("
        s_sql_info['ZOMBIE'] = "insert into QualityMonitorZomBieInfo(gataway_id,\
                            zombie_proc,record_date) values"
        s_sql_info['CORE_MODULE'] = "insert into QualityMonitorCoreModuleInfo(\
                            gataway_id,core_module_info,record_date) values"
        s_sql_info['CORE_PROCESS'] = "insert into QualityMonitorCoreProcInfo(\
                            gataway_id,core_proc_info,record_date) values"
        s_sql_info['CORE_CONF'] = "insert into QualityMonitorCoreConfInfo(\
                            gataway_id,core_conf_info,record_date) values"
        s_sql_info['CPU'] = "insert into QualityMonitorCPUAndMemInfo(\
                            gataway_id , cpu_info, mem_info , record_date) values"
        s_sql_info['STORAGE_CHECK'] = "insert into QualityMonitorStorageHardWareInfo(\
                            gataway_id ,content,record_date) values"
        s_sql_info['OPENED_PORT'] = "insert into QualityMonitorOpenPortInfo(\
                            gataway_id ,port_info,record_date) values"
        s_sql_info['DCLOG_SIZE'] = "insert into QualityMonitorLogInfo(\
                            gataway_id ,log_info,record_date) values"
        s_sql_info['CORE_DUMP'] = "insert into QualityMonitorCoreProcInfo(\
                            gataway_id,core_dump_proc,record_date,core_dump_path) values"
        s_sql_info['EXCEPT'] = "insert into QualityMonitorExecptionInfo(\
                            gataway_id,zombie_proc_info,execpt_reboot_info,\
                            core_dump_info,cpu_mem_info,core_proc_info,core_module_info,\
                            core_cfg_info,except_account_info,record_date) values"
        return s_sql_info                    

    def sql_proc_entry(self,dict,flag):
        if not dict:
            return True
        print 'start to proc data tables '
        self.dev_id = dict['BASE']['dev_id']
        self.record_date = datetime.datetime.strptime(dict['BASE']['device_time'],'%Y%m%d %H:%M:%S')

        self.exec_base_table_data(dict,flag)
        self.exec_except_table_data(dict)
        self.common_module_proc_table(dict)
        self.exec_cpu_and_mem_info(dict)
        self.exec_storage_check_table_data(dict)
        self.exec_dclog_table_data(dict)
        
    def show_parse_data(self,data):
        if self.debug_flag == 1:
            print data
        
    def common_data_proc(self,dict,name):
        if not dict or  not dict[name]:
            return ""
        common_data = {}
        common_data = dict[name]
        return 	common_data

    def strcat_sql(self,data):
        ''''''
        if not data:
            return ""
        common_data_info = ""
        key_len = len(data)
        for index  in range(1,key_len + 1 , 1):
            common_data_info += "('%s','%s','%s')" %(self.dev_id,data[index],self.record_date)
            if index != key_len:
                common_data_info += ','
        return common_data_info		
        
    def get_sql_values(self,dict,name):
        '''¸ù¾Ý½âÎö³öÀ´µÄÖµ½øÐÐsql×Ö·û´®µÄÆ´½Ó''' 
        common_data = self.common_data_proc(dict,name)
        if not common_data :
            return ""
            
        self.show_parse_data(common_data)	
        return self.strcat_sql(common_data)
    
    def exec_sql_opr(self,sql_str):
        '''¿¿¿¿¿¿¿¿¿¿'''
        if not sql:
            print '¿¿¿¿¿¿¿¿¿¿¿'
            raise
 #       print sql_str    
        try:
            sql.sql_exec(sql_str)
        except:
            raise
        return True

    def exec_base_table_data(self,dict,flag):
        '''»ù±¾±í´¦ÀíÐÅÏ¢'''
        if not dict:
            return True
        base_info = {}
        base_info = self.common_data_proc(dict,'BASE')
        if not base_info:
            return False
        sql_str = "%s'%s','%s','%s','%s','%s','%s','%s','%s','%s|%s','%s','%s','%s')" %(\
                   self.sql_info['BASE'], base_info['dev_id'],
                               base_info['customer'] ,
                               base_info['hard_plat'],
                               base_info['device_ip'],
                               base_info['crash_time'],
                               base_info['run_time'],
                               base_info['device_time'],
                               base_info['device_plat'],
                               base_info['storage_plat'],
                               dict['STORAGE_CHECK']['capacity'],
                               base_info['device_version'],
                               self.record_date ,flag)
        return self.exec_sql_opr(sql_str)
        

    def get_last_insert_sql(self,name,common_sql_info):
        '''»ñÈ¡×îºó¿ÉÒÔ²åÈëµ½Êý¾Ý¿âÖÐµÄsql'''
        sql_str = self.sql_info[name] + common_sql_info
        return 	self.exec_sql_opr(sql_str)
        
    def common_proc_table_data(self,dict,name):
        common_sql_info = self.get_sql_values(dict,name)
        if not common_sql_info:
            return False

        self.show_parse_data(common_sql_info)
        return self.get_last_insert_sql(name,common_sql_info)	
     
    def common_module_proc_table(self,dict):
        '''Í¨ÓÃÄ£¿é´¦ÀíÐÅÏ¢'''
        module_list = ['ZOMBIE' , 'CORE_DUMP','CORE_MODULE',\
                        'CORE_PROCESS','CORE_CONF','OPENED_PORT']
        module_list_len = len(module_list)
        for index in range(module_list_len):
            self.common_proc_table_data(dict,module_list[index])
        return True    
        

    def exec_cpu_and_mem_info(self,dict):
        '´¦ÀíÒì³£CPU»òÕßÊÇÒì³£ÄÚ´æÐÅÏ¢'
        
        cpu_info = {}
        mem_info = {}
        sql_cpu_info = ""
        sql_mem_info = ""
        cpu_info = self.common_data_proc(dict,'CPU')
        mem_info = self.common_data_proc(dict,'MEM')
        if not cpu_info and not mem_info:
            return True
        self.show_parse_data(mem_info)
        if cpu_info:
            sql_cpu_info = cpu_info['CPU']
        if mem_info:
            sql_mem_info  = mem_info['MEM']
        sql_str = "%s(%s,%s,%s,%s)" %(self.sql_info['CPU'],self.dev_id, \
                                           sql_cpu_info,\
                                           sql_mem_info,\
                                           self.record_date)
        return self.exec_sql_opr(sql_str)
        
    def exec_storage_check_table_data(self,dict):
        '´¦Àí´æ´¢Ó²¼þÒì³£'
        dict['STORAGE_CHECK'].pop('type')
        if 'capacity' in dict['STORAGE_CHECK'].keys():
            dict['STORAGE_CHECK'].pop('capacity')
        return self.common_proc_table_data(dict,'STORAGE_CHECK')
        
    def exec_dclog_table_data(self,dict):
        '´¦ÀíÒì³£ÄÚÖÃÊý¾ÝÖÐÐÄÈÕÖ¾'
        
        dclog_info = dict['DCLOG_SIZE']
        for key,value in dclog_info.items():
            if not value:
                continue
            str = key.split('_')
            self.record_date = str[1]
            dclog_sql_info = self.get_sql_values(dclog_info,key)
            if not dclog_sql_info:
                return False
            self.get_last_insert_sql('DCLOG_SIZE',dclog_sql_info)
        return True	
        
    def createTableSql(self,info):
        ''''''
        s_except_sql = "('%s',%d,%d,%d,%d,%d,%d,%d,%d,'%s');" %(\
                        self.dev_id,info['ZOMBIE'],info['EXCEPT_REBOOT'],\
                        info['CORE_DUMP'],info['CORE_MODULE'],info['CORE_PROCESS'],\
                        info['CPU'],info['CORE_CONF'],\
                        info['ABNORMAL_USER'],self.record_date
                        )

        
        s_except_sql = self.sql_info['EXCEPT'] + s_except_sql
     #   print s_except_sql
        
        
        return self.exec_sql_opr(s_except_sql)
        
    def exec_except_table_data(self,dict):
        '''½«ÓÐÎÊÌâµÄÊý¾Ý·Å½øÒì³£±í'''
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
      #  print 	except_info	

        self.createTableSql(except_info)
        
        return True	
        

if __name__ == '__main__':
    sql.con_db()
    db_handle = DbDataOpr()
    dict = {'CORE_MODULE': {1: 'exclude no insmod', 2: 'dosck_drv no insmod', 3: 'sf_pcre no insmod'}, 'CORE_PROCESS': {1: 'fluxctrld no exists'}, 'MEM': {}, 'CORE_CONF': {}, 'ZOMBIE': {1: '[cleancore.sh]', 2: '[sec_event_check]', 3: '[python]'}, 'BASE': {'customer': '\xe8\x81\x94\xe5\x8c\x96\xe7\xa7\x91\xe6\x8a\x80\xe8\x82\xa1\xe4\xbb\xbd\xe6\x9c\x89\xe9\x99\x90\xe5\x85\xac\xe5\x8f\xb8', 'dev_id': '65812D44', 'device_time': '20160810 02:00:01', 'device_plat': '4G2C', 'device_ip': '10.251.251.251', 'hard_plat': 'version=2015.10.19.1003 provider=xinhan type=H61 model=AF-1720', 'crash_time': 'Crashed time:2012-02-14 23:48:41', 'run_time': '0 days', 'storage_plat': 'SSD', 'device_version': ''}, 'STORAGE_CHECK': {1: '/dev/root /orig/dev/sinfor ext3 ro,relatime,errors=continue,data=writeback 0 0', 2: 'tmpfs /fwlog/ip_sess_count/often_write tmpfs rw,relatime,size=2048k 0 0', 3: '/dev/sys /sys sysfs rw,relatime 0 0', 4: 'tmpfs /var/often_write tmpfs rw,relatime,size=4096k 0 0', 5: '/dev/sda6 /fwlog ext3 rw,noatime,errors=continue,data=ordered 0 0', 6: 'tmpfs /var/tmp/kvfilter tmpfs rw,relatime,size=102400k 0 0', 7: '/dev/sda3 /fwlib ext3 rw,noatime,errors=continue,data=ordered 0 0', 8: '/dev/root /orig/lib64 ext3 ro,relatime,errors=continue,data=writeback 0 0', 9: '/dev/root /orig/var ext3 ro,relatime,errors=continue,data=writeback 0 0', 10: 'tmpfs /var/often_read tmpfs rw,relatime,size=4096k 0 0', 11: 'tmpfs /var/run tmpfs rw,relatime,size=2048k 0 0', 12: '/dev/sda3 /usr ext3 rw,noatime,errors=continue,data=ordered 0 0', 13: 'tmpfs /fwlog/log_data/tmp tmpfs rw,relatime,size=20480k 0 0', 14: 'tmpfs /var/tmp/darkchain tmpfs rw,relatime,size=20480k 0 0', 15: '/dev/sda3 /dev/sinfor ext3 rw,noatime,errors=continue,data=ordered 0 0', 16: '/dev/sda3 /sbin ext3 rw,noatime,errors=continue,data=ordered 0 0', 17: '/dev/sda3 /lib64 ext3 rw,noatime,errors=continue,data=ordered 0 0', 18: '/dev/root / ext3 ro,relatime,errors=continue,data=writeback 0 0', 19: 'shm /dev/shm tmpfs rw,nosuid,nodev,relatime 0 0', 20: 'none /dev/pts devpts rw,relatime,gid=5,mode=620 0 0', 21: 'tmpfs /fwlog/ads/spider/rtinfo tmpfs rw,relatime,size=2048k 0 0', 22: '/dev/sda3 /var ext3 rw,noatime,errors=continue,data=ordered 0 0', 23: '/dev/root /orig/etc ext3 ro,relatime,errors=continue,data=writeback 0 0', 24: '/dev/root /orig/bin ext3 ro,relatime,errors=continue,data=writeback 0 0', 25: 'tmpfs /fwlog/ads/redir_cache tmpfs rw,relatime,size=30720k 0 0', 26: '/dev/sda3 /bin ext3 rw,noatime,errors=continue,data=ordered 0 0', 27: '/proc /proc proc rw,relatime 0 0', 28: 'rootfs / rootfs rw 0 0', 29: '/dev/root /orig/sbin ext3 ro,relatime,errors=continue,data=writeback 0 0', 30: '/dev/root /orig/usr ext3 ro,relatime,errors=continue,data=writeback 0 0', 31: '/dev/sda1 /boot ext3 ro,noatime,errors=continue,data=ordered 0 0', 32: '/dev/sda3 /etc ext3 rw,noatime,errors=continue,data=ordered 0 0', 'capacity': '128G', 'type': 'SSD'}, 'OPENED_PORT': {1: 'udp,0,0,0.0.0.0:51111,0.0.0.0:*,', 2: 'tcp,0,0,0.0.0.0:8001,0.0.0.0:*,LISTEN', 3: 'udp,0,0,0.0.0.0:33141,0.0.0.0:*,', 4: 'tcp,0,0,0.0.0.0:54322,0.0.0.0:*,LISTEN', 5: 'tcp,0,1,60.191.148.244:45029,113.105.88.58:80,SYN_SENT', 6: 'udp,0,0,0.0.0.0:1813,0.0.0.0:*,', 7: 'tcp,0,0,0.0.0.0:800,0.0.0.0:*,LISTEN', 8: 'udp,0,0,0.0.0.0:54878,0.0.0.0:*,', 9: 'tcp,0,0,0.0.0.0:80,0.0.0.0:*,LISTEN', 10: 'tcp,0,0,0.0.0.0:8000,0.0.0.0:*,LISTEN', 11: 'tcp,0,0,0.0.0.0:443,0.0.0.0:*,LISTEN', 12: 'tcp,0,0,0.0.0.0:22345,0.0.0.0:*,LISTEN', 13: 'raw,0,0,0.0.0.0:112,0.0.0.0:*,112', 14: 'raw,188800,0,0.0.0.0:112,0.0.0.0:*,112', 15: 'tcp,0,0,0.0.0.0:54321,0.0.0.0:*,LISTEN', 16: 'tcp,0,0,0.0.0.0:851,0.0.0.0:*,LISTEN', 17: 'udp,0,0,0.0.0.0:52000,0.0.0.0:*,', 18: 'tcp,0,0,0.0.0.0:51111,0.0.0.0:*,LISTEN', 19: 'udp,0,0,0.0.0.0:1980,0.0.0.0:*,', 20: 'tcp,0,0,0.0.0.0:85,0.0.0.0:*,LISTEN', 21: 'udp,0,0,0.0.0.0:123,0.0.0.0:*,', 22: 'tcp,0,0,0.0.0.0:4420,0.0.0.0:*,LISTEN', 23: 'tcp,0,0,0.0.0.0:442,0.0.0.0:*,LISTEN', 24: 'udp,0,0,0.0.0.0:811,0.0.0.0:*,', 25: 'udp,0,0,0.0.0.0:48096,0.0.0.0:*,', 26: 'tcp,0,0,0.0.0.0:81,0.0.0.0:*,LISTEN', 27: 'udp,0,0,0.0.0.0:44321,0.0.0.0:*,', 28: 'tcp,0,0,60.191.148.244:39908,183.134.16.90:80,TIME_WAIT', 29: 'udp,0,0,0.0.0.0:51614,0.0.0.0:*,', 30: 'udp,0,0,0.0.0.0:35585,0.0.0.0:*,', 31: 'tcp,0,0,0.0.0.0:850,0.0.0.0:*,LISTEN'}, 'DCLOG_SIZE': {'DCLOG_20160807': {}, 'DCLOG_20160806': {}, 'DCLOG_20160805': {1: '/fwlog/log_data/fwlog/20160805,168.0K', 2: '/fwlog/log_data/fwlog/20160805/read_status,4.0K', 3: '/fwlog/log_data/fwlog/20160805/frm,160.0K'}, 'DCLOG_20160809': {1: '/fwlog/log_data/fwlog/20160809/frm,160.0K', 2: '/fwlog/log_data/fwlog/20160809/C,16.0K', 3: '/fwlog/log_data/fwlog/20160809,216.0K', 4: '/fwlog/log_data/fwlog/20160809/X,20.0K', 5: '/fwlog/log_data/fwlog/20160809/read_status,16.0K'}, 'DCLOG_20160808': {1: '/fwlog/log_data/fwlog/20160808/frm,160.0K', 2: '/fwlog/log_data/fwlog/20160808/read_status,4.0K', 3: '/fwlog/log_data/fwlog/20160808,168.0K'}, 'DCLOG_20160810': {1: '/fwlog/log_data/fwlog/20160810,168.0K', 2: '/fwlog/log_data/fwlog/20160810/read_status,4.0K', 3: '/fwlog/log_data/fwlog/20160810/frm,160.0K'}}, 'CORE_DUMP': {}, 'CPU': {}, 'ABNORMAL_USER': {}}
	#exec_except_table_data(dict)
    db_handle.sql_proc_entry(dict,1)
								
