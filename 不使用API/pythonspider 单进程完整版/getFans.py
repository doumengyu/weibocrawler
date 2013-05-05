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


class getFans:
    charset = 'utf8'
    uid = '';
    path='C:/weibodata'
    pageNum = 0     #粉丝共有多少页
    
    def get_fans(self,uid):
        fanslist=[]
        self.uid = uid
        url = self.get_url(uid)
        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
        text = result.read()
        content = eval("u\"\"\" "+text+"\n \"\"\" ").encode(getFans.charset)
        self.get_totallPageNum(content)
        i=1
        while i<getFans.pageNum+1 and i<51:
            url = self.get_url(uid,i)
            i+=1
            try:
                req = urllib2.Request(url)
                result = urllib2.urlopen(req)
                text = result.read()
            except Exception: 
                continue
            pattern = re.compile('<script>STK && STK.pageletM && STK.pageletM.view\((.*?)\)<\/script>')
            result = pattern.findall(text)
            jsonResult = json.loads(result[7])  #粉丝信息所在result
            soup = BeautifulSoup(jsonResult['html'])
            try:
                idlist=soup.findAll('a',attrs={'class': "W_f14 S_func1"})
                for ids in idlist:
                    id=ids['usercard']
                    fanslist.append(id)
            except Exception as e:
                pass
        for fans in fanslist:
            self.writefile(self.path+'/'+self.uid+'_fans.txt',fans+'\n')   
        
        

    def get_totallPageNum(self,content):
        tag1 = '<strong node-type=\"fans\">'
        pos1 = content.find(tag1)+len(tag1)
        tag2 = '<\/strong>'
        pos2 = content.find(tag2,pos1)
        getFans.pageNum = int(float(content[pos1:pos2]))
        getFans.pageNum = getFans.pageNum/20+1
    
    def get_url(self,uid,page=1):
        url = 'http://weibo.com/' + uid + '/fans?page='+str(page)
        return url
    def writefile(self,filename,content):
        fw = file(filename,'a')
        fw.write(content)
        fw.close()

    