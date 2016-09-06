#!/usr/sbin/env python
#-*- coding:utf-8 -*-

import common
import os

class M15appcoreParse(object):
    def __init__(self):
        self.key = 'M15appcore'
        self.module_filename = ''
    def run(self,dirpath, file):
        self.common = common.Common()
        root_path = self.common.createDirByKey(file , self.key)

        filelist = os.listdir(dirpath)
        for zipfile in filelist:
            cmd = "unzip -jxo " + dirpath + '/' +zipfile + ' -d ' + root_path
            print 'cmd :',cmd
            rtn = os.system(cmd)
            if rtn == 0 :
                filename = dirpath + '/' +zipfile
            os.remove(filename)	
        return True
