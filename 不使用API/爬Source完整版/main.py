#!/usr/bin/env python
# -*- coding: utf-8 -*-

import weiboLogin
import getWeiboPage
import urllib
import urllib2
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def get_uid(filename,uid_list):
    fread = file(filename)
    for line in fread:
        uid_list.append(line.strip())

def writefile(filename,content):
    fw = file(filename,'a')
    fw.write(content)
    fw.close()


if __name__ == '__main__':
    username = ''
    pwd = ''
    WBLogin = weiboLogin.weiboLogin()
    if(WBLogin.login(username, pwd)=='servertime_error'):
        print 'login failed. check out your network.'
        sys.exit()
    uid_list=[]
    get_uid('C:/Result1.txt',uid_list)
    path='C:/weibodata'
    if not os.path.exists(path):
        os.mkdir(path)
    for uid in uid_list:
        try:
            WBpage = getWeiboPage.getWeiboPage()
            WBpage.get_msg(uid)
           
        except Exception as e:
            writefile('C:/id.txt',str(uid)+'\n')

