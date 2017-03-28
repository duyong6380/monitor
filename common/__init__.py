#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-

modules_name = ['aoam_download','aoam_uncompress']

import aoam_download
import aoam_uncompress
from aoam_common import log

def module_init():
    '''
        brief:主要是模块初始化
    '''
    for module in modules_name:
        try:
            eval(module).init()
        except Exception,err:
            log("init module %s failed" %module)
            return False
    return True

def module_run(argv):
    '''
        breief:主要是控制模块的运行
    '''
    for module in modules_name:
        try:
            eval(module).run()
        except Exception,err:
            log("run module %s failed,err %s" %(module,err))
            return False
    return True

def module_exec(argv,flag=0):
    return (module_init() if flag==0 else module_run(argv))
    
if __name__ == "__main__":
    module_exec("",0)
    module_exec("",1)
        
