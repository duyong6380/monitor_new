#!/usr/sbin/env python
#coding:UTF-8
import logging  as log


'ÈÕÖ¾¼ÇÂ¼´°¿Ú'
log_format = '%(filename)s,lineno:%(lineno)d [%(asctime)s] %(message)s'
log.basicConfig(format = log_format,datefmt='%Y-%m-%d %H:%M:%S %p',\
                filename='/var/log/uploadMonitor.log',level=log.INFO)


if __name__ == '__main__':
    log.info("hello,this is world")
