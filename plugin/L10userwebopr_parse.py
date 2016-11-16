#!/usr/sbin/env python
#-*- coding:utf-8 -*-

import sys
import common.common as common

class L10userweboprParse(object):
    def __init__(self):
        self.key = 'L10userwebopr'
        self.module_filename = 'user_data_collect.ini'
    def run(self,dirname , file):
        self.common = common.Common()
        return self.common.common_proc(dirname , file ,self.key ,self.module_filename )

if __name__ == '__main__':
    file = '/var/duyong/saasdata/file_data/20161114/L10userwebopr_7.0/DF/F7/DFF7EE30/1479060043_L10userwebopr_7.0_1_1.470331392_1000_ODg2Mg=='
    dirname = '/tmp/after/L10userwebopr'
    handle = L10userweboprParse()
    handle.run(dirname , file)
