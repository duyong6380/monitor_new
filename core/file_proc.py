#!/usr/sbin/env python
#-*- coding:utf-8 -*-

import os 
import re
import sys

sys.path.append('../')
from common import logProc as log

def write_to_file(dst_file,src_file,dirname):
	dst_file = dirname + '/' + dst_file	+ '_temp'
	src_file = dirname + '/' + src_file
	
	if os.path.exists(src_file) == False or dst_file == src_file:
		return ""
	
	try:		
		src_f = open(src_file,'r+')
		dst_f = open(dst_file , "a+")
		for eachline in src_f:
			dst_f.write(eachline)
	except IOError as e:	
		log.error("open file failed ")
	src_f.close()
	dst_f.close()	
	return os.path.basename(dst_file)

def getSplitNum(strs):
	'''
	返回值：
	1、结束
	2、不结束
	'''
	file_index = strs[4].split('.')
	if int(file_index[0]) > int(strs[3]):
		return 0
	return file_index[0]

def getMergeFileName(file_dict,dirname):
	file_list = []
	filename_tmp = ""
	for key,value in file_dict.items():
		length = len(value)
		for index in range(1,len(value)+1 , 1):
			strs = value[str(index)].split('_')
			if int(strs[3]) != length:
				break
			#print 'filename:',value[str(index)]
			filename_tmp = write_to_file(strs[0],value[str(index)] ,dirname)
		
		if filename_tmp != "":
			file_list.append(filename_tmp)
	return 	file_list
	
def updateDictFileList(strs, filename,dict_file):	
	new_dict_info = {}
	index = getSplitNum(strs)
	if len(dict_file) == 0:
		new_dict_info[index] = filename
		return new_dict_info
		
	#print 'dict_file:',dict_file
	
	if strs[0] not in dict_file.keys():
		dict_file[strs[0]] = {}
	new_dict_info = dict_file[strs[0]]
	
	
	new_dict_info[index] = filename
	return new_dict_info
		

def merge_mutil_file_to_one(dirname ,list_dir_file):
	'''
	 对于多重切分文件进行合并
	'''
	new_file_list = []
	mutil_file_list = {}
	filename_list = []
	for filename in list_dir_file:
		#print 'filename:',filename
		strs = filename.split('_')
		if len(strs) != 7:
			continue
		
		if strs[3] == '1':
			new_file_list.append(filename)
			continue
		'''根据时间戳和切分块来进行字典排列，必须保证是顺序索引进行排列的'''
		#print 'file_list:',mutil_file_list
		mutil_file_list[strs[0]] = updateDictFileList(strs , filename,mutil_file_list)
		
		
	filename_list = getMergeFileName(mutil_file_list,dirname)
	
	if len(filename_list) == 0:
		return new_file_list
		
	for filelist in filename_list:
		new_file_list.append(filelist)
	return 	new_file_list

if __name__ == "__main__":
    dirname = "/var/duyong/saasdata/file_data/20161114/L10userwebopr_7.0/DF/F7/DFF7EE30"
    list_info = ['1479060043_L10userwebopr_7.0_1_1.470331392_1000_ODg2Mg==']
    new_list = []
    new_list = merge_mutil_file_to_one(dirname,list_info)
    print '=================================='
    print 'mew_list :',new_list
    print '==================================='
