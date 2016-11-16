#!/usr/sbin/env python
#coding:UTF-8

'''
±¾½Å±¾µÄ¹¦ÄÜ£º
1¡¢½âÑ¹ÎÄ¼þ
2¡¢Ö´ÐÐ»Øµ÷
'''
import os 
import sys
import tarfile
import time
import datetime

class Common(object):
    def __init__(self):
        self.unzip_save_dir = '/tmp/after/'
        self.upload_storage_dir = '/var/log_data/appcore/'

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
        if key == "":
            return ""
        dev_id = self.getDevIdByPath(file)
        if dev_id == "":
            return ""

        time_str = time.strftime('%Y%m%d',time.localtime(time.time()))
        root_dir = self.upload_storage_dir + key + '/' + time_str + '/' + dev_id
        
        if os.path.exists(root_dir) == False:
            os.makedirs(root_dir)
        return root_dir	
            
		
if __name__ == '__main__':
    filelist = ['/var/duyong/L05info_7.0/20160919/02/9C/029C991F/1468519207_L05info_7.0_1_1.470134784_1000_ODgxOA==', '/var/duyong/L05info_7.0/20160919/02/9C/029C991F/1467741608_L05info_7.0_1_1.470044672_1000_NTI3MQ==', '/var/duyong/L05info_7.0/20160919/02/9C/029C991F/1468951208_L05info_7.0_1_1.470134784_1000_NDczOA==', '/var/duyong/L05info_7.0/20160919/02/9C/029C991F/1468260008_L05info_7.0_1_1.470134784_1000_ODc1Ng==', '/var/duyong/L05info_7.0/20160919/02/9C/029C991F/1468432807_L05info_7.0_1_1.470134784_1000_Mzc3Mg==', '/var/duyong/L05info_7.0/20160919/02/9C/029C991F/1468864808_L05info_7.0_1_1.470134784_1000_MzAwNw==', '/var/duyong/L05info_7.0/20160919/02/9C/029C991F/1469037610_L05info_7.0_1_1.470134784_1000_NDIxNA==', '/var/duyong/L05info_7.0/20160919/02/9C/029C991F/1468778407_L05info_7.0_1_1.470134784_1000_NjAyMg==', '/var/duyong/L05info_7.0/20160919/02/9C/029C991F/1468692009_L05info_7.0_1_1.470134784_1000_NTE0NA==', '/var/duyong/L05info_7.0/20160919/02/9C/029C991F/1467655209_L05info_7.0_1_1.470044672_1000_OTc2NA==', '/var/duyong/L05info_7.0/20160919/02/9C/029C991F/1468346410_L05info_7.0_1_1.470134784_1000_MTEz', '/var/duyong/L05info_7.0/20160919/02/9C/029C991F/1468605607_L05info_7.0_1_1.470134784_1000_NDA5NQ==']
    common_handle = Common()
    key = 'L05info'
    common_handle.common_parse_hook(filelist,key)
	
