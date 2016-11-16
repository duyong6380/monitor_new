#!/usr/sbin/env python
#coding:UTF-8

'''
±¾½Å±¾µÄ¹¦ÄÜ£º
1¡¢½âÑ¹ÎÄ¼þ
2¡¢Ö´ÐÐ»Øµ÷
import L05info_parse
import M10crashlog_parse
import L10userwebopr_parse
import M05applog_parse
import M15appcore_parse
'''
import sys
sys.path.append('../')
import zipfile
from plugin import *
import logging as log 
import os 
import tarfile
import time
import datetime

dir_key_info = ['L05info','M10crashlog','L10userwebopr','M05applog','M15appcore']

def get_date(last_record_date,date_flag = 0):
    last_date = last_record_date
    today_date = datetime.datetime.today()
    today_date = today_date.strftime('%Y%m%d')

    if not last_date :
       last_date = str(int(today_date) - 7)
    if int(today_date) <= int(last_date):
        raise StateExcept("日期不正确，当前时间小于上次处理时间")
    
    date_list = []
    int_last_date = int(last_date)
    int_today_date = int(today_date)
    if date_flag == 1:
        return str(int_today_date - 1)
    while int_last_date < int_today_date:
          int_last_date = int_last_date + 1
          date_list.append(str(int_last_date))
    
    return  date_list  
def getRemoteFile(last_record_date):
    date_list = get_date(last_record_date)
    if not date_list:
        return False
    print date_list
    remote_file_pre = '/'
    local_file_pre = '/var/duyong/'
    remote_ip_list = '_20.10.1.37'
    file_pre = 'file_data_'
    filelist = []
    for date in date_list:
        file_name = file_pre + date + remote_ip_list + '.tar.gz' 
        remote_file_path = remote_file_pre + file_name
        local_file_path = local_file_pre + file_name
        print 'remote_file_path:',remote_file_path,'local:',local_file_path
        if not os.path.exists(local_file_path):
            filelist.append(remote_file_path)
    print filelist
    return filelist

class Common(object):
    def __init__(self):
        self.unzip_save_dir = '/tmp/after/'
        self.upload_storage_dir = '/var/log_data/appcore/'
        self.parse_cb = self.common_init();

    def common_init(self):
        parse_cb = {}
        global dir_key_info
        key_len = len(dir_key_info)
        for index in range(key_len):
            classname = dir_key_info[index] + '_parse'+'.'+dir_key_info[index]+'Parse'
            cb_hanle = dir_key_info[index] + 'handle'
            cb_handle = eval(classname)()
       #     print 'cb.key:',cb_hanle.key
            parse_cb[dir_key_info[index]] = cb_handle

        return parse_cb

    def delTempFile(self,filelist):
        ''' É¾³ýÁÙÊ±´æ´¢µÄÎÄ¼þ'''
        for filename in filelist:
            tmp_name = os.path.basename(filename)
            strs = tmp_name.split('_')
            if len(strs) == 2 and strs[1] == 'temp': 
                os.remove(filename)
        return True		
    def printf(self,str):
        if not str:
            print str

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
        
    def construct_unrar_cmd(self,filename,dir,num):
        cmd = "tar xvf " + filename + " --strip-components " +  str(num) + " -C " + dir + " >>/dev/null"
        return cmd
        
    def uncompress(self,key,file_path):
        tmp_unzip_save_dir = self.unzip_save_dir + key
        print 'tmp_unzip_save_dir:',tmp_unzip_save_dir
        if os.path.exists(tmp_unzip_save_dir) == False:
            os.makedirs(tmp_unzip_save_dir)
        try:
            fz = zipfile.ZipFile(file_path,mode='r')

            for file_name in fz.namelist():
                fz.extract(file_name,tmp_unzip_save_dir)
        except:
            num = 3
            if key == 'L10userwebopr':
                num = 2
            cmd = self.construct_unrar_cmd(file_path,tmp_unzip_save_dir,num)
            os.system(cmd)
        return tmp_unzip_save_dir	

    def common_parse_hook(self,filelist , key):
        '''¸ù¾Ý¼üÖµÀ´»Øµ÷¶ÔÓ¦µÄ¹³×Óº¯Êý'''
        #print 'key:',key
        for file in filelist:
            print 'common:',file
            parse_dir = self.uncompress(key , file)
            if parse_dir == "":
                return False
            print 'parse_dir:',parse_dir
            try:
                self.parse_cb[key].run(parse_dir,file)
            except:
                print '¿¿¿¿[%s]¿¿¿¿[%s]¿¿' %(key,parse_dir)
                raise
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
    filelist = ['']
    common_handle = Common()
    key = 'L10userwebopr'
    common_handle.common_parse_hook(filelist,key)
	
