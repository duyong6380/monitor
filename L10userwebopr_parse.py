#!/usr/sbin/env python
#-*- coding:utf-8 -*-

import common

class L10userweboprParse(object):
    def __init__(self):
        self.key = 'L10userwebopr'
        self.module_filename = 'user_data_collect.ini'
    def run(self,dirname , file):
        self.common = common.Common()
        return self.common.common_proc(dirname , file ,self.key ,self.module_filename )

