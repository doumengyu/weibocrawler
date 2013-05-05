#! /usr/bin/env python
#coding=utf-8

import urllib
import urllib2
import sys
import time
import re
import socket
import json
from bs4 import BeautifulSoup


socket.setdefaulttimeout(60)

reload(sys)
sys.setdefaultencoding('utf-8')

class getFollowers:
    charset = 'utf8'
    uid = '';
    path='C:/weibodata'
    pageNum = 0     #关注的人共有多少页
    
    def get_followers(self,uid):
        followerlist=[]
        self.uid = uid
        url = self.get_url(uid)
        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
        text = result.read()
        content = eval("u\"\"\" "+text+"\n \"\"\" ").encode(getFollowers.charset)
        self.get_totallPageNum(content)
        i=1
        while i<getFollowers.pageNum+1:
            url = self.get_url(uid,i)
            i+=1
            req = urllib2.Request(url)
            result = urllib2.urlopen(req)
            text = result.read()
            pattern = re.compile('<script>STK && STK.pageletM && STK.pageletM.view\((.*?)\)<\/script>')
            result = pattern.findall(text)
            jsonResult = json.loads(result[8])  #关注的人信息所在result
            soup = BeautifulSoup(jsonResult['html'])
            try:
                idlist=soup.findAll('a',attrs={'class': "W_f14 S_func1"})
                for ids in idlist:
                    id=ids['usercard']
                    followerlist.append(id)
            except Exception as e:
                pass
        for follower in followerlist:
            self.writefile(self.path+'/'+self.uid+'_follow.txt',follower[3:]+'\n')   
        
        
    def get_totallPageNum(self,content):
        tag1 = '<strong node-type=\"follow\">'
        pos1 = content.find(tag1)+len(tag1)
        tag2 = '<\/strong>'
        pos2 = content.find(tag2,pos1)
        getFollowers.pageNum = int(float(content[pos1:pos2]))
        getFollowers.pageNum = getFollowers.pageNum/20+1
    
    def get_url(self,uid,page=1):
        url = 'http://weibo.com/' + uid + '/follow?page='+str(page)
        return url
    def writefile(self,filename,content):
        fw = file(filename,'a')
        fw.write(content)
        fw.close()
    
    
