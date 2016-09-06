#!/usr/sbin/env python
#coding=utf-8

import commands
import sys
import os
import logProc as log
import getFilename as gfn
import common
import re
import file_proc
import shutil


UPLOAD_PARSE_LOCK_FILE = '/var/lock/upload_monitor.lock'
s_rootdir = "/var/duyong/"

class UploadParseMain(object):
    def __init__(self):
       self.com_handle =  self.init_func()
       self.root_dir = '/var/duyong/'
    def parse_entry(self):
        self.exec_func()
        self.exit_func()
    def exit_func(self):
        pass
    def exec_func(self):
        '''¶ÔÔÆ¶ËÏÂÔØµÄÎÄ¼ş½øĞĞ½âÎö×ÜÈë¿Úº¯Êı£¬Ö÷Òª¹¦ÄÜÈçÏÂ£º
        1¡¢½âÑ¹Êı¾İ
        2¡¢Õë¶ÔÃ¿¸öÄ¿Â¼µ÷ÓÃÏàÓ¦µÄ½âÎöº¯Êı½øĞĞ½âÎö
        '''
        dir_list_info = {}
        dir_list_info = gfn.GetDirInfo(s_rootdir)
        #print dir_list_info
        for dir_key,dir_value in dir_list_info.items():
            try :
                self.parse_one_dir_file(dir_key,dir_list_info)
            except:
                log.error("func_name[exec_func]Ö´ĞĞ´íÎó" )
                return False
        return True		


    def get_data_from_cloud(self):
        ''' ´ÓÔÆ¶Ë»ñÈ¡ĞèÒª½âÎöµÄÊı¾İ,ÔİÊ±²»×ö'''
        pass
    def check_db_table_create(self):
        ''''''
        pass
        
    def init_func(self):
        '''Ö´ĞĞ½âÎöµÄ³õÊ¼»¯º¯Êı£ºÖ÷Òª¹¦ÄÜÈçÏÂ£º
        ¢´ÓÔÆ¶Ë×Ô¶¯»ñÈ¡µ±ÌìĞèÒª½âÎöµÄÊı¾İ
        ¢¼ì²éÏàÓ¦µÄÊı¾İ¿âÊÇ·ñÒÑ¾­´´½¨
        '''
        self.get_data_from_cloud()
        self.check_db_table_create()
        com_handle = common.Common()
        return com_handle
            

    def parse_one_dir_file(self,dir_key ,dir_list_info):
        '''½âÎöÒ»¸öÄ¿Â¼ÏÂµÄÎÄ¼ş'''
        for dirname in dir_list_info[dir_key]:
            FileList = []
            #print '-------FileList:',FileList
            
            print dirname 
            if dir_key != 'L05info':
                return True
            print dir_key 
            
            list_file = os.listdir(dirname)
            print 'list_file:%s , dirname:%s' %(list_file,dirname)
            new_file = file_proc.merge_mutil_file_to_one(dirname ,list_file)
            if len(new_file) == 0 :
                return False
                
            print 'new_file:',new_file	
            print dirname
            
            for file in new_file:
                FileList.append(os.path.join(dirname,file))

            try :
                print 'FileList:',FileList
                self.com_handle.common_parse_hook(FileList,dir_key)
                self.com_handle.delTempFile(FileList)
                '''
                if dir_key == 'L05info':
                    sys.exit(1)
                '''    
            except:
                print "¿¿[%s]¿¿¿¿" %(dir_key)
                sys.exit(1)
        return True
        
# ÓÃÎÄ¼şËøÊµÏÖ½ø³Ìµ¥Àı, ±£Ö¤µ¥ÀıÔËĞĞ, Èç¹ûÒÑ¾­ÓĞ½ø³Ìµ÷ÓÃ»¹Ã»ÍË³ö£¬¾Í»áÍË³ö
# func          : ²¶×¥Òì³£µÄ²Ù×÷
def single_process_run(func):
	'''²¶×¥ÎÄ¼şËøÒì³££¬ÅĞ¶ÏÊÇ·ñµ¥½ø³Ì'''
	global UPLOAD_PARSE_LOCK_FILE
	
	try:
		import fcntl
		f = open(UPLOAD_PARSE_LOCK_FILE, 'w')
		fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
	except Exception, e:
		f.close()
		func_name = func.__name__
		log.error('func_name:%s ÒÑ¾­´æÔÚÒ»¸öÊµÀıÔÚÔËĞĞ' %func_name)
		sys.exit(1)
	func() 
	fcntl.flock(f, fcntl.LOCK_UN)
	f.close()
    
def main():
    '''ÖÊÁ¿¼à¿Ø½âÎöÖ÷º¯ÊıÈë¿Ú'''
    parse_handle = UploadParseMain()
    single_process_run(parse_handle.parse_entry)

if __name__ == '__main__':
	main()
