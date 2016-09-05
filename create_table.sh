#!/bin/bash


function create_table()
{
	
	mysqlCall='mysql -uroot -proot FW_LOG_fwlog -e'
	
	local TABLE_NAME=$1
	local create_sql="$2"
	
	local drop_sql="DROP TABLE IF EXISTS $TABLE_NAME"
	
	${mysqlCall} "$drop_sql"
	if [ $? -ne 0 ];then
		echo "exec drop table $TABLE_NAME failed"
		exit -1
	fi
	${mysqlCall} "$create_sql"
	if [ $? -ne 0 ];then
		echo "exec create $TABLE_NAME failed"
		exit -1
	fi
	return 0
}


function create_base_table()
{
	TABLE_NAME_BASE="QualityMonitorBaseInfo"
	create_sql_baseinfo="CREATE TABLE \`$TABLE_NAME_BASE\` (
			  \`auto_id\` int(10) unsigned NOT NULL AUTO_INCREMENT,
			  \`gataway_id\` varchar(8) NOT NULL DEFAULT 0,
			  \`dev_name\` varchar(512) NOT NULL DEFAULT 0,
			  \`hw_info\` varchar(200) NOT NULL DEFAULT 0,
			  \`dev_ip\` binary(16) NOT NULL,
			  \`last_crash_time\` varchar(48) NOT NULL ,
			  \`days_run\` varchar(20) NOT NULL DEFAULT 0,
			  \`upload_time\` varchar(48) NOT NULL,
			  \`dev_platform\` varchar(5) NOT NULL DEFAULT 0,
			  \`storage_platform\` varchar(10) NOT NULL DEFAULT 0,
			  \`version\` varchar(30) NOT NULL DEFAULT 0,
			  \`except_flag\` varchar(2) NOT NULL DEFAULT 0,
			  \`record_date\` datetime  NOT NULL,
			  PRIMARY KEY (\`gataway_id\`,\`record_date\`),
			  KEY \`index_name\` (\`auto_id\`,\`dev_name\`,\`hw_info\`,\`dev_ip\`,\`upload_time\`,\`dev_platform\`,\`storage_platform\`,\`version\`)
			) ENGINE=MyISAM DEFAULT CHARSET=latin1"
		

	create_table $TABLE_NAME_BASE "$create_sql_baseinfo"
}


function create_execpt_table()
{
	TABLE_NAME_EXECPTTION="QualityMonitorExecptionInfo"
	
	create_sql_execptionInfo="CREATE TABLE \`$TABLE_NAME_EXECPTTION\` (
			  \`auto_id\` int(10) unsigned NOT NULL AUTO_INCREMENT,
			  \`gataway_id\` varchar(8) NOT NULL DEFAULT 0,
			  \`zombie_proc_info\` int(1) NOT NULL DEFAULT 0,
			  \`execpt_reboot_info\` int(1) NOT NULL DEFAULT 0,
			  \`core_dump_info\` int(1) NOT NULL DEFAULT 0,
			  \`cpu_mem_info\` int(1) NOT NULL DEFAULT 0,
			  \`hd_info\` int(1) NOT NULL DEFAULT 0,
			  \`core_proc_info\` int(1) NOT NULL DEFAULT 0,
			  \`core_module_info\` int(1) NOT NULL DEFAULT 0,
			  \`core_cfg_info\` int(1) NOT NULL DEFAULT 0,
			  \`open_port_info\` int(1) NOT NULL DEFAULT 0,
			  \`except_account_info\` int(1) NOT NULL DEFAULT 0,
			  \`log_info\` int(1) NOT NULL DEFAULT 0,
			  \`record_date\` datetime  NOT NULL,
			  PRIMARY KEY (\`gataway_id\`,\`record_date\`),
			  KEY \`index_name\` (\`auto_id\`,\`record_date\`)
			) ENGINE=MyISAM DEFAULT CHARSET=latin1"
	create_table $TABLE_NAME_EXECPTTION "$create_sql_execptionInfo"		
}

function create_zombie_info()
{
	TABLE_NAME="QualityMonitorZomBieInfo"
	
	create_sql_Info="CREATE TABLE \`$TABLE_NAME\` (
			  \`auto_id\` int(10) unsigned NOT NULL AUTO_INCREMENT,
			  \`gataway_id\` varchar(8) NOT NULL DEFAULT 0,
			  \`zombie_proc\` varchar(64) NOT NULL DEFAULT 0,
			  \`record_date\` datetime  NOT NULL,
			  PRIMARY KEY (\`gataway_id\`,\`zombie_proc\`,\`record_date\`),
			   KEY \`index_name\` (\`auto_id\`)
			) ENGINE=MyISAM DEFAULT CHARSET=latin1"
	create_table $TABLE_NAME "$create_sql_Info"		
}

function core_dump_info()
{
	TABLE_NAME="QualityMonitorCoreDumpInfo"
	
	create_sql_Info="CREATE TABLE \`$TABLE_NAME\` (
			  \`auto_id\` int(10) unsigned NOT NULL AUTO_INCREMENT,
			  \`gataway_id\` varchar(8) NOT NULL DEFAULT 0,
			  \`core_dump_proc\` varchar(64) NOT NULL DEFAULT 0,
			  \`record_date\` datetime  NOT NULL,
			  \`core_dump_path\` varchar(64) NOT NULL DEFAULT 0,
			  PRIMARY KEY (\`gataway_id\`,\`core_dump_proc\`,\`record_date\`),
			   KEY \`index_name\` (\`auto_id\`)
			) ENGINE=MyISAM DEFAULT CHARSET=latin1"
	create_table $TABLE_NAME "$create_sql_Info"	
}


function storage_platform_info()
{
	TABLE_NAME="QualityMonitorStorageHardWareInfo"
	
	create_sql_Info="CREATE TABLE \`$TABLE_NAME\` (
			  \`auto_id\` int(10) unsigned NOT NULL AUTO_INCREMENT,
			  \`gataway_id\` varchar(8) NOT NULL DEFAULT 0,
			  \`content\` varchar(512) NOT NULL DEFAULT 0,
			  \`record_date\` datetime  NOT NULL,
			  PRIMARY KEY (\`gataway_id\`,\`content\`,\`record_date\`),
			   KEY \`index_name\` (\`auto_id\`)
			) ENGINE=MyISAM DEFAULT CHARSET=latin1"
	create_table $TABLE_NAME "$create_sql_Info"	
}


function core_proc_info()
{
	TABLE_NAME="QualityMonitorCoreProcInfo"
	
	create_sql_Info="CREATE TABLE \`$TABLE_NAME\` (
			  \`auto_id\` int(10) unsigned NOT NULL AUTO_INCREMENT,
			  \`gataway_id\` varchar(8) NOT NULL DEFAULT 0,
			  \`core_proc_info\` varchar(64) NOT NULL DEFAULT 0,
			  \`record_date\` datetime  NOT NULL,
			  PRIMARY KEY (\`gataway_id\`,\`core_proc_info\`,\`record_date\`),
			   KEY \`index_name\` (\`auto_id\`)
			) ENGINE=MyISAM DEFAULT CHARSET=latin1"
	create_table $TABLE_NAME "$create_sql_Info"	
}

function core_module_info()
{
	TABLE_NAME="QualityMonitorCoreModuleInfo"
	
	create_sql_Info="CREATE TABLE \`$TABLE_NAME\` (
			  \`auto_id\` int(10) unsigned NOT NULL AUTO_INCREMENT,
			  \`gataway_id\` varchar(8) NOT NULL DEFAULT 0,
			  \`core_module_info\` varchar(64) NOT NULL DEFAULT 0,
			  \`record_date\` datetime  NOT NULL,
			  PRIMARY KEY (\`gataway_id\`,\`core_module_info\`,\`record_date\`),
			   KEY \`index_name\` (\`auto_id\`)
			) ENGINE=MyISAM DEFAULT CHARSET=latin1"
	create_table $TABLE_NAME "$create_sql_Info"	
}

function core_conf_info()
{
	TABLE_NAME="QualityMonitorCoreConfInfo"
	
	create_sql_Info="CREATE TABLE \`$TABLE_NAME\` (
			  \`auto_id\` int(10) unsigned NOT NULL AUTO_INCREMENT,
			  \`gataway_id\` varchar(8) NOT NULL DEFAULT 0,
			  \`core_conf_info\` varchar(64) NOT NULL DEFAULT 0,
			  \`record_date\` datetime  NOT NULL,
			  PRIMARY KEY (\`gataway_id\`,\`core_conf_info\`, \`record_date\`),
			   KEY \`index_name\` (\`auto_id\`)
			) ENGINE=MyISAM DEFAULT CHARSET=latin1"
	create_table $TABLE_NAME "$create_sql_Info"	
}

function open_port_info()
{
	TABLE_NAME="QualityMonitorOpenPortInfo"
	
	create_sql_Info="CREATE TABLE \`$TABLE_NAME\` (
			  \`auto_id\` int(10) unsigned NOT NULL AUTO_INCREMENT,
			  \`gataway_id\` varchar(8) NOT NULL DEFAULT 0,
			  \`port_info\` varchar(256) NOT NULL DEFAULT 0,
			  \`record_date\` datetime  NOT NULL,
			  PRIMARY KEY (\`gataway_id\`,\`port_info\`,\`record_date\`),
			   KEY \`index_name\` (\`auto_id\`)
			) ENGINE=MyISAM DEFAULT CHARSET=latin1"
	create_table $TABLE_NAME "$create_sql_Info"	
}	

function except_account_info()
{
	TABLE_NAME="QualityMonitorAccountInfo"
	
	create_sql_Info="CREATE TABLE \`$TABLE_NAME\` (
			  \`auto_id\` int(10) unsigned NOT NULL AUTO_INCREMENT,
			  \`gataway_id\` varchar(8) NOT NULL DEFAULT 0,
			  \`account_info\` varchar(128) NOT NULL DEFAULT 0,
			  \`record_date\` datetime  NOT NULL,
			  PRIMARY KEY (\`gataway_id\`,\`record_date\`),
			   KEY \`index_name\` (\`auto_id\`)
			) ENGINE=MyISAM DEFAULT CHARSET=latin1"
	create_table $TABLE_NAME "$create_sql_Info"	
}	

function detail_log_info()
{
	TABLE_NAME="QualityMonitorLogInfo"
	
	create_sql_Info="CREATE TABLE \`$TABLE_NAME\` (
			  \`auto_id\` int(10) unsigned NOT NULL AUTO_INCREMENT,
			  \`gataway_id\` varchar(8) NOT NULL DEFAULT 0,
			  \`log_info\` varchar(512) NOT NULL DEFAULT 0,
			   \`record_date\` datetime  NOT NULL,
			  PRIMARY KEY (\`gataway_id\`,\`log_info\`,\`record_date\`),
			   KEY \`index_name\` (\`auto_id\`)
			) ENGINE=MyISAM DEFAULT CHARSET=latin1"
	create_table $TABLE_NAME "$create_sql_Info"	
}
	  
function cpu_and_mem_info()
{
	TABLE_NAME="QualityMonitorCPUAndMemInfo"
	
	create_sql_Info="CREATE TABLE \`$TABLE_NAME\` (
			  \`auto_id\` int(10) unsigned NOT NULL AUTO_INCREMENT,
			  \`gataway_id\` varchar(8) NOT NULL DEFAULT 0,
			  \`cpu_info\` varchar(64) NOT NULL DEFAULT 0,
			  \`mem_info\` varchar(64) NOT NULL DEFAULT 0,
			   \`record_date\` datetime  NOT NULL,
			  PRIMARY KEY (\`gataway_id\`,\`record_date\`),
			   KEY \`index_name\` (\`auto_id\`)
			) ENGINE=MyISAM DEFAULT CHARSET=latin1"
	create_table $TABLE_NAME "$create_sql_Info"	
}


function create_table_main()
{
	create_base_table 
	create_execpt_table
	create_zombie_info
	detail_log_info
	except_account_info
	storage_platform_info
	core_proc_info
	core_module_info
	core_conf_info
	open_port_info
	core_dump_info
	cpu_and_mem_info
}
create_table_main
