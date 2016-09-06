#!/usr/sbin/env python
#coding:UTF-8

'''
本脚本的功能：
1、解压文件
2、执行回调
'''
import L05info_parse
import M10crashlog_parse
import L10userwebopr_parse
import M05applog_parse
import M15appcore_parse
import logging as log 
import os 
import sys
import tarfile
import time

dir_key_info = ['L05info','M10crashlog','L10userwebopr','M05applog','M15appcore']

class Common(object):
    def __init__(self):
        self.unzip_save_dir = '/tmp/after/'
        self.upload_storage_dir = '/var/log_data/appcore/'
        self.parse_cb = self.common_init();

    def common_init(self):
        parse_cb = {}
        global dir_key_info
        key_len = len(dir_key_info)
        for index in range(key_len):
            classname = dir_key_info[index] + '_parse'+'.'+dir_key_info[index]+'Parse'
            cb_hanle = dir_key_info[index] + 'handle'
            cb_handle = eval(classname)()
       #     print 'cb.key:',cb_hanle.key
            parse_cb[dir_key_info[index]] = cb_handle

        return parse_cb

    def delTempFile(self,filelist):
        ''' 删除临时存储的文件'''
        for filename in filelist:
            tmp_name = os.path.basename(filename)
            strs = tmp_name.split('_')
            if len(strs) == 2 and strs[1] == 'temp': 
                os.remove(filename)
        return True		
    def printf(self,str):
        if not str:
            print str

    def common_proc(self,dirname , file , s_key_value , s_module_filename):
        root_path = self.createDirByKey(file , s_key_value )
        if root_path == "" :
            return False
            
        cmd = 'cp -rf ' + dirname + '/' + s_module_filename + ' ' + root_path
        
        #print 'cmd :',cmd
        rtn = os.system(cmd)
        if rtn == 0:
            filename = dirname + '/' + s_module_filename
            os.remove(filename)
        return True
        
    def construct_unrar_cmd(self,filename,dir,num):
        cmd = "tar xvf " + filename + " --strip-components " +  str(num) + " -C " + dir + " >>/dev/null"
        return cmd
        
    def uncompress(self,key,file_path):
        tmp_unzip_save_dir = self.unzip_save_dir + key
        print 'tmp_unzip_save_dir:',tmp_unzip_save_dir
        if os.path.exists(tmp_unzip_save_dir) == False:
            os.makedirs(tmp_unzip_save_dir)
        num = 3
        if key == 'L10userwebopr':
            num = 2
        try:
            cmd = self.construct_unrar_cmd(file_path,tmp_unzip_save_dir,num)
            os.system(cmd)
        except:
            self.printf('unzip file:' + file_path)
            return ""  
        return tmp_unzip_save_dir	

    def common_parse_hook(self,filelist , key):
        '''根据键值来回调对应的钩子函数'''
        #print 'key:',key
        for file in filelist:
            print 'common:',file
            parse_dir = self.uncompress(key , file)
            if parse_dir == "":
                return False
            print 'parse_dir:',parse_dir
            try:
                self.parse_cb[key].run(parse_dir,file)
            except:
                print '靠靠[%s]靠靠[%s]靠' %(key,parse_dir)
                raise
        return True

    def getDevIdByPath(self,file):
        if file == "":
            return ""

        dev = os.path.dirname(file)
        if dev == "":
            return ""
        dev = os.path.basename(dev)
        if dir == "":
            return ""
        return dev	
        
    def createDirByKey(self,file , key):
        global s_upload_storage_rootdir
        if key == "":
            return ""
        dev_id = self.getDevIdByPath(file)
        if dev_id == "":
            return ""

        time_str = time.strftime('%Y%m%d',time.localtime(time.time()))
        root_dir = s_upload_storage_rootdir + key + '/' + time_str + '/' + dev_id
        
        if os.path.exists(root_dir) == False:
            os.makedirs(root_dir)
        return root_dir	
            
		
if __name__ == '__main__':
    filelist = ['/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1471629603_L05info_7.0_1_1.470179840_1000_OTMxNQ==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1472407204_L05info_7.0_1_1.470179840_1000_OTQ4NA==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1472666405_L05info_7.0_1_1.470179840_1000_NTEwMQ==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1470592803_L05info_7.0_1_1.470179840_1000_MTIzNg==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1471284004_L05info_7.0_1_1.470179840_1000_Mjk5Ng==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1470765603_L05info_7.0_1_1.470179840_1000_NjUzOA==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1470506404_L05info_7.0_1_1.470179840_1000_NjEyOQ==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1472580005_L05info_7.0_1_1.470179840_1000_NDIwMg==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1471975203_L05info_7.0_1_1.470179840_1000_NTkwMQ==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1472320803_L05info_7.0_1_1.470179840_1000_MTM2Mw==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1470938405_L05info_7.0_1_1.470179840_1000_NTgxNA==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1472493604_L05info_7.0_1_1.470179840_1000_NDQzMA==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1471111204_L05info_7.0_1_1.470179840_1000_NDAxMw==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1472148003_L05info_7.0_1_1.470179840_1000_NTAwMg==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1470852004_L05info_7.0_1_1.470179840_1000_Njk4MQ==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1471716003_L05info_7.0_1_1.470179840_1000_NTMwMA==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1470679204_L05info_7.0_1_1.470179840_1000_OTY4NA==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1472061603_L05info_7.0_1_1.470179840_1000_MjM3NQ==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1471802403_L05info_7.0_1_1.470179840_1000_OTU5Mw==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1472752804_L05info_7.0_1_1.470179840_1000_NTY4OQ==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1471370403_L05info_7.0_1_1.470179840_1000_NjM=', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1471888804_L05info_7.0_1_1.470179840_1000_ODIy', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1472234404_L05info_7.0_1_1.470179840_1000_Njk5Nw==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1471456804_L05info_7.0_1_1.470179840_1000_MzY4Mg==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1471197604_L05info_7.0_1_1.470179840_1000_NzQ0Mg==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1471024803_L05info_7.0_1_1.470179840_1000_NTEwNA==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1471543203_L05info_7.0_1_1.470179840_1000_OTgwOA==', '/var/duyong/L05info_7.0/FC/B9/FCB9D9D4/1470420004_L05info_7.0_1_1.470179840_1000_MjU4Nw==']
    common_handle = Common()
    key = 'L05info'
    common_handle.common_parse_hook(filelist,key)
	
