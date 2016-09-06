#!/usr/sbin/env python
#-*- coding:utf-8 -*-

import common


class M10crashlogParse(object):
    def __init__(self):
        self.key = 'M10crashlog'
        self.module_filename = 'sys_crash.txt'
    def run(self,dirname , file):
        self.common = common.Common()
        return self.common.common_proc(dirname , file ,self.key ,self.module_filename )

