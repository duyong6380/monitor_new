#!/usr/sbin/env python
#-*- coding=utf8 -*-

import urllib2 as url
#import urllib
import json

def send_json(data):
    ''''''
    url_str = 'http://200.200.194.155:9200/af_view/bugreport/'
 #   headers = {'Content-Type': 'application/json', "charset": "utf-8"}
    #data = urllib.urlencode(json_data)
    #json_data = json.dumps(data)
    json_data = json.dumps(data,ensure_ascii=False)
    print json_data
    f_handle = url.urlopen(url_str,json_data)
    print f_handle.read()


if __name__ == '__main__':
    json_str = {"僵尸进程": "[python]"}
    json_str = json.dumps(json_str,ensure_ascii=False)#.encode('UTF-8')
    print json_str
  #  print type(json_str)
    send_json(json_str)


