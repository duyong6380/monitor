#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
进程daemon化
"""

from __future__ import print_function

import os
import sys


def daemon():
    """
    Breif: 进程daemon化流程
    """
    # 产生子进程，而后父进程退出
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, errorinfo:
        sys.stderr.write('fork #1 failed: %d (%s)\n' % (
            errorinfo.errno, errorinfo.strerror))
        sys.exit(1)

    # 创建新的会话，子进程成为会话的首进程
    os.setsid()
    # 修改子进程工作目录
    os.chdir("/")
    # 重新设置文件权限
    os.umask(0)

    # 创建孙子进程，而后子进程退出 -
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, err:
        sys.stderr.write('fork #2 failed: %d (%s)\n' % (
            err.errno, err.strerror))
        sys.exit(1)

    # 重定向标准输入流、标准输出流、标准错误
    sys.stdout.flush()
    sys.stderr.flush()
    si = file("/dev/null", 'r')
    so = file("/dev/null", 'a+')
    se = file("/dev/null", 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
