#!/usr/sbin/env python
#coding:UTF-8


import sys
sys.path.append('/home/duyong/duyong_git/monitor/quality_control')
import commands
import os
import getFilename as gfn
from common import *
import re
import file_proc
import shutil
import datetime
import time
from config import cfg_info
from stateExcept import StateExcept

from autodownload import FtpDownload

UPLOAD_PARSE_LOCK_FILE = '/var/lock/upload_monitor.lock'
       
class UploadParseMain(object):
    def __init__(self):
        self.init_func()
    def parse_entry(self):
        self.exec_func()
        self.exit_func()
    def exit_func(self):
        pass   
    def exec_func(self):
        try:
            self.ftp_download.getRemoteData()
            print '====从云端下载成功,休眠5秒之后进行解析==================='
            time.sleep(5)
        except:
            raise StateExcept("从云端下载数据失败，退出")
        
        dir_list_info = {}
        dir_list_info = gfn.GetDirInfo(self.config)
        #print '===',dir_list_info
        for dir_key,dir_value in dir_list_info.items():
            if not dir_value:
                continue
            #print '***',dir_key,dir_value
            try :
                self.parse_one_dir_file(dir_key,dir_value)
            except:
                StateExcept("func_name[exec_func]执行解析失败" )
        return True		
        
    def init_func(self):
        self.config = cfg_info.getSectionConfig()
        self.ftp_download = FtpDownload(self.config)
        self.com_handle = common.Common()
    def getParseFileList(self,dirname):
        ''''''
        FileList = []
        list_file = os.listdir(dirname)
        new_file = file_proc.merge_mutil_file_to_one(dirname ,list_file)
        if len(new_file) == 0 :
            return False

        for file in new_file:
            FileList.append(os.path.join(dirname,file))
            
        return FileList    
        
    def parse_one_dir_file(self,dir_key ,dir_list_info):
        ''''''
        for dirname in dir_list_info:
            FileList = []
            FileList = self.getParseFileList(dirname)
            if not FileList:
                return True
            
            try :
             #   print 'FileList:',FileList
                self.com_handle.common_parse_hook(FileList,dir_key)
                self.com_handle.delTempFile(FileList)
            except:
                print "模块[%s]解析失败" %(dir_key)
                sys.exit(1)
        return True
         
def single_process_run(func):
	'''²¶×¥ÎÄ¼þËøÒì³££¬ÅÐ¶ÏÊÇ·ñµ¥½ø³Ì'''
	global UPLOAD_PARSE_LOCK_FILE
	
	try:
		import fcntl
		f = open(UPLOAD_PARSE_LOCK_FILE, 'w')
		fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
	except Exception, e:
		f.close()
		func_name = func.__name__
		log.error('func_name:%s ÒÑ¾­´æÔÚÒ»¸öÊµÀýÔÚÔËÐÐ' %func_name)
		sys.exit(1)
	func() 
	fcntl.flock(f, fcntl.LOCK_UN)
	f.close()
    
def main():
    '''ÖÊÁ¿¼à¿Ø½âÎöÖ÷º¯ÊýÈë¿Ú'''
    parse_handle = UploadParseMain()
    single_process_run(parse_handle.parse_entry)

if __name__ == '__main__':
	main()
