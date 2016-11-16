#!/usr/sbin/env python


import os
import sys
class OldUploadProc(object):
    def __init__(self):
        print 'hello,world'       
    def run(self,dirname=None):
        try:
            os.system("sh getfile.sh")
        except:
            print sys.exc_info()
            raise
        return True 


        



if __name__ == '__main__':
    handle = OldUploadProc()
    handle.run()

