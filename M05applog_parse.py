#!/usr/sbin/env python
#-*- coding:utf-8 -*-

import common

class M05applogParse(object):
    def __init__(self):
        self.key = 'M05applog'
        self.module_filename = 'app_log.log'
    def run(self,dirname , file):
        self.common = common.Common()
        return self.common.common_proc(dirname , file ,self.key ,self.module_filename )



