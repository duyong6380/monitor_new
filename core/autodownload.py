#!/usr/bin/env python
# -*- coding: utf-8 -*-
from  ftplib import FTP
import os
import sys
from config import cfg_info
from stateExcept import StateExcept
import re
from common.common import (get_date,getRemoteFile)

class FTPSync(object):
    conn = FTP()
    def __init__(self,host,port = 21):    
        self.conn.connect(host,port)
    def login(self,username,password):
        try:
            self.conn.login(username,password)
        except:
            raise StateExcept("ftp login failed,please retry again")
        self.conn.set_pasv(False)
        print self.conn.welcome

    def get_ftp_dirname(self,ftp_path):
        return self.conn.nlst(ftp_path)

    def _is_ftp_file(self,ftp_path):
        '''判断ftp路径是否是文件'''
        print "14445888888"
        try:
            print self.conn.nlst(ftp_path)
        except:
            print sys.exc_info()
            raise
        try:
          if ftp_path in self.conn.nlst(ftp_path):
            return True
          else:
            return False
        except ftplib.error_perm,e:
          return False
    def _ftp_list(self, line):
        '''根据远程目录判断需要获取是目录还是文件'''
        list = line.split(' ')
        if self.ftp_dir_name==list[-1] and list[0].startswith('d'):
            self._is_dir = True
    '''         
    def _is_ftp_dir(self,ftp_path):
        ftp_path = ftp_path.rstrip('/')
        ftp_parent_path = os.path.dirname(ftp_path)
        self.ftp_dir_name = os.path.basename(ftp_path)
        #print 'parent:%s,dirname:%s' %(ftp_parent_path,self.ftp_dir_name)
        self._is_dir = False
        if ftp_path == '.' or ftp_path== './' or ftp_path=='':
          self._is_dir = True
        else:
          #this ues callback function ,that will change _is_dir value
          try:
            self.conn.retrlines('LIST %s' %ftp_parent_path,self._ftp_list)
          except :
            return self._is_dir    
        return self._is_dir
    '''

    def get_file(self,ftp_path,local_path='.'):

        ftp_path = ftp_path.rstrip('/')
        print ftp_path
        if self._is_ftp_file(ftp_path):    
          print '========='
          file_name = os.path.basename(ftp_path)
          #如果本地路径是目录，下载文件到该目录
          if os.path.isdir(local_path):
            file_handler = open(os.path.join(local_path,file_name), 'wb' )
            self.conn.retrbinary("RETR %s" %(ftp_path), file_handler.write) 
            file_handler.close()
          #如果本地路径不是目录，但上层目录存在，则按照本地路径的文件名作为下载的文件名称
          elif os.path.isdir(os.path.dirname(local_path)):
            file_handler = open(local_path, 'wb' )
            self.conn.retrbinary("RETR %s" %(ftp_path), file_handler.write) 
            file_handler.close()
          #如果本地路径不是目录，且上层目录不存在，则退出
          else:
            print 'EROOR:The dir:%s is not exist' %os.path.dirname(local_path)
        else:
          print '111'
          print 'EROOR:The ftp file:%s is not exist' %ftp_path
        print '12111'
    
    def createLocalDir(self,ftp_path,local_path,begin):
        ''''''
        if begin :
           local_path=os.path.join(local_path,os.path.basename(ftp_path))
        if not os.path.isdir(local_path):
          os.makedirs(local_path)
        return local_path

    def get_dir(self,ftp_path,local_path='.',begin=True): 
        ftp_path = ftp_path.rstrip('/')

        if self._is_ftp_dir(ftp_path):
          #进入ftp目录，开始递归查询
          local_path = self.createLocalDir(ftp_path,local_path,begin)
          
          self.conn.cwd(ftp_path)
          ftp_files = self.conn.nlst()

          for file in ftp_files:
            local_file = os.path.join(local_path, file)
          #  print 'local_file:',local_file
            #fftp_path = os.path.join(ftp_path,file)
            if self._is_ftp_dir(file):
              self.get_dir(file,local_file,False)
            else:
              self.get_file(file,local_file)
          self.conn.cwd( ".." )
        return True

    def close(self):
      self.conn.quit()
      
class FtpDownload(FTPSync):
    '''根据配置信息进行实际的下载操作'''
    def __init__(self,config):
        self.setClassAttr(config)
        self.ftp_handle = super(FtpDownload,self)
        self.ftp_handle.__init__(self.FTP_INFO['ip'],self.FTP_INFO['port'])

    def setClassAttr(self,config):
        for setting in config:
            if setting.isupper() and isinstance(setting,str):
                setting_value = config[setting]
                setattr(self,setting,setting_value)
        
    def ftp_download(self,remote_file):  
        for filename in remote_file:
            try:
                self.ftp_handle.get_file(filename,self.ROOT_DIR)
            except:
                raise StateExcept("ftp download failed , dir:",filename)
            finally:
                self.ftp_handle.close()        
                return False
        return True

    def getRemoteData(self):
        print '==================='
        try:
            self.ftp_handle.login(self.FTP_INFO['username'],self.FTP_INFO['password'])
        except:
            print sys.exc_info()
            raise
        remote_file = getRemoteFile(self.LAST_RECORD_DATE)
        if not remote_file:
            return False
        print remote_file
        print '111111111111111111111111====='
        return self.ftp_download(remote_file)    
 
if __name__ == '__main__':
  '''  
  ftp = FTPSync('127.0.0.1',21)
  ftp.login('duyong','woshishui')
  ftp.get_dir('/home/duyong/L05info_*/20160908/','/var/duyong')
  ftp.close()
  '''
  config_info = cfg_info.getSectionConfig()
  print config_info
  ftp_hook = FtpDownload(config_info)
  #ftp_hook.getRemoteData()
  ftp_hook.getRemoteData()
