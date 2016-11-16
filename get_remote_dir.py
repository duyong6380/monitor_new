#!/usr/sbin/env python


import monitor as setting
import datetime
class DIR_OPR(object):
    def __init__(self,config):
        self.config = config

    def get_date(self):
        last_date = self.config['LAST_RECORD_DATE']
        today_date = datetime.datetime.today()
        today_date = today_date.strftime('%Y%m%d')

        if int(today_date) <= int(last_date):
            return ""
        return today_date   

    def getRemoteDir(self):
        ''''''
        dir_info = {}
        remote_dir = self.config['FTP']['remote_root_dir']
        today_date = self.get_date()
        print today_date
        if today_date == "":
            return ""
        for name in self.config['TABLE']:
            dir_info[name] =  remote_dir+ ' /' + name + '_*/' + today_date 
        return dir_info

    def getRemoteData(self):
        ''''''
        remoteDir = {}
        remoteDir = self.getRemoteDir()
        if not remoteDir:
            return ""
        return  remoteDir

if __name__ == '__main__':
    config_info = {'FTP': {'username': 'duyong', 'ip': '127.0.0.1', 'remote_root_dir': '/home/duyong', 'localdir': '/var/duyong', 'password': 'woshishui', 'port': 21}, 'LAST_RECORD_DATE': '20160908', 'TABLE': ['L05info', 'M10crashlog', 'L10userwebopr', 'M05applog', 'M15appcore']}
    dir_opr = DIR_OPR(config_info)
    print dir_opr.getRemoteData()
