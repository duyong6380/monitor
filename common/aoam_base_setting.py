#!/usr/bin/env  python
#coding:UTF-8


LOG_PATH = "/var/log/aoam"  # 错误日志目录
LOG_MAX_SIZE = 1048576  # 日志文件最大限定为1M

ROOT_DIR = '/var/duyong'
SAVE_PATH_DIR = '/tmp/after'

FTP_INFO = {
		'host':"222.126.229.182",
		'port':8021,
		'username':"oprt_data",
		'password':"opdt_2016@sxfAf!1115",
		'localdir':"/var/duyong",
		'remote_root_dir':"/",
        'timeout':300
		}

KEY_TABLE = ['L05info','M10crashlog','L10userwebopr','M05applog','M15appcore']

DATE_LEN = 8  # 日期长度20151214
DEBUG = 1 #日志调试开关

