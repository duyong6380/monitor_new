#!/usr/sbin/env python
#coding:utf8
import sys
sys.path.append('../')
#from stateExcept import StateExcept
CONFIG_NAME = 'setting.settings'

class Config(object):
    def __init__(self):
        '''获取配置文件解析句柄'''
        self.init_config()

    def init_config(self):
        '''初始化配置信息'''
        __import__(CONFIG_NAME)
        mod = sys.modules[CONFIG_NAME]
        
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod,setting)
                setattr(self, setting, setting_value)    
                
    def getSectionConfig(self,name=None):
        '''显示配置文件中的配置信息字典
            如果name为空，则显示全部配置信息，否则，显示
            特定的信息
        '''
        if name is  None:
            return vars(self)
        if hasattr(self,name) == False:    
            raise StateExcept("config file is not exist attrbuite [%s]" %name)
        return getattr(self,name)

cfg_info = Config()
if __name__ == '__main__':
    print cfg_info.getSectionConfig('FTP_INFO')
