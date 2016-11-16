#!/usr/sbin/env python
#coding:UTF-8

import os
import sys
import re
import tarfile
from config import cfg_info
from common.common import (get_date,getRemoteFile)

def GetDirFilename(FindPath,table_list):
    dir_info = {}
    file_list = []
    for tablename in table_list:
        file_list = []
        for dir in os.listdir(FindPath):
            if re.search(tablename, dir) is not None and dir != 'L05info_10':
                file_list.append(os.path.join(FindPath,dir))
        dir_info[tablename] = file_list
    return  dir_info
	
def GetFileListByDirName(dirname):
    src_root_dir = []
    dst_root_dir = []
	
    for root,dirs,files in os.walk(dirname):
        for filespath in files:
            src_root_dir.append(root)
    dst_root_dir = list(set(src_root_dir))
    return dst_root_dir	  
	
def GetAllFileList(dir_dict,config):
    '''根据日期获取对应的路径下文件'''
    dir_file_info = {}
    dir_list = []

    for key,value in dir_dict.items():
        dir_list = []
        for dir_name in value:
            dir_file_name = GetFileListByDirName(dir_name)
            if not dir_file_name:
                continue
            for file_path in dir_file_name:
                dir_list.append(file_path)
        
        if not dir_list:
            dir_file_info[key] = {}
            continue
        dir_file_info[key] =  dir_list 
        
    return dir_file_info

def GetDirInfo(config):
    dir_info = {}
    for filename in getRemoteFile(config['LAST_RECORD_DATE']):
        last_file = config['ROOT_DIR'] + filename
     #   print last_file
        if not os.path.exists(last_file):
            continue
        print '++++====+++++++'
        tar = tarfile.open(last_file)
        for names in tar.getnames():
            tar.extract(names,path=config['ROOT_DIR'])
        tar.close()
    table_list = []
    rootdir = config['ROOT_DIR'] + '/saasdata/file_data/' + get_date("",1)
    print rootdir
    table_list = config['KEY_TABLE']
    dir_info = GetDirFilename(rootdir,table_list)
    return GetAllFileList(dir_info,config)
	
if __name__ == '__main__':
    config = cfg_info.getSectionConfig()
    print config
    GetDirInfo(config)
	 
