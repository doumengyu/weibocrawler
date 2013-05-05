#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import weiboLogin
import getWeiboPage
import getInfo
import getFollowers
import getFans
import urllib
import urllib2
import os
import sys
import threading

reload(sys)
sys.setdefaultencoding('utf-8')

def get_uid(filename,uid_list):
    fread = file(filename)
    for line in fread:
        uid_list.append(line.strip())
        #time.sleep(1)

class crawl(threading.Thread):
    def __init__(self, num,uids):  
        threading.Thread.__init__(self)  
        self.thread_num = num
        self.uids=uids
        
    def run(self): 
        #WBpage = getWeiboPage.getWeiboPage()
        #InfoPage=getInfo.getInfo()
        FollowsPage=getFollowers.getFollowers()
        #FansPage=getFans.getFans()
        for uid in self.uids:
            try:
                #WBpage.get_msg(uid)
                #InfoPage.get_info(uid)
                FollowsPage.get_followers(uid)
                #FansPage.get_fans(uid)
            except Exception as e:
                pass
            

if __name__ == '__main__':
    username = ''
    pwd = ''
    threadnum=1   #爬取新浪微博的线程数目
    uid_list=[]
    get_uid('C:/Result1.txt',uid_list)
    divide=len(uid_list)/threadnum
    uid_split=[uid_list[i:i+divide] for i in range( 0,len(uid_list),threadnum)]
    WBLogin = weiboLogin.weiboLogin()
    if(WBLogin.login(username, pwd)=='servertime_error'):
        print 'login failed. check out your network.'
        sys.exit()
    path='C:/weibodata'
    if not os.path.exists(path):
        os.mkdir(path)
    i=0
    while i<threadnum:
        thread = crawl(i,uid_split[i])
        thread.start() 
        i+=1
        
    


