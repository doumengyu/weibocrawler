#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

class getWeiboPage:
    body = {
        '__rnd':'', #访问这一页面的时间，以秒表示的13位整数，貌似可以设置为空
        '_k':'', #本次登录第一次访问此微薄的时间，16位整数，貌似可以设置为空
        '_t':'0', #不知道是什么
        'count':'50', #第二次和第二次访问时都是15，第一次访问时是50
        'end_id':'', #最新的这一项微博的mid，也就是本页最上面的微博的mid，貌似也可以设置为空
        'max_id':'', #已经见到的，也就是目前能看到的最下面微博的mid，貌似也可以设置为空
        'page': 1, #微博的第几页
        'pagebar':'', #第二次是0，第三次是1，第一次没有这项
        'pre_page':'0', #第二次和第三次都是本页页码，第一次访问是上页页码
        'uid':'' #博主的uid'
    }
    uid_list = []
    charset = 'utf8'
    pageNum = 0     #微博总共有多少页
    flag = 0
    uid = ''
    path='C:/weibodata'
    def get_msg(self,uid):
        self.uid = uid
        getWeiboPage.flag = 0
        getWeiboPage.pageNum = 0
        getWeiboPage.body['uid'] = uid
        getWeiboPage.body['page'] = 1
        url = self.get_url(uid)
        self.get_firstpage(url)
        self.get_secondpage(url)
        self.get_thirdpage(url)
        i = 2
        while i<getWeiboPage.pageNum+1 and i<20:
            getWeiboPage.body['page'] = i
            self.get_firstpage(url)
            self.get_secondpage(url)
            self.get_thirdpage(url)
            i = i+1
    def get_totallPageNum(self,content):
        tag1 = '<strong node-type=\"weibo\">'
        pos1 = content.find(tag1)+len(tag1)
        tag2 = '<\/strong>'
        pos2 = content.find(tag2,pos1)
        #print '**************' + str(pos1)
        #print '**************' + str(pos2)
        getWeiboPage.pageNum = int(float(content[pos1:pos2]))
        getWeiboPage.pageNum = getWeiboPage.pageNum/45+1
        #print '微博总共有 '+str(getWeiboPage.pageNum)+' 页'
        #time.sleep(99)
    def get_firstpage(self,url):
        getWeiboPage.body['pre_page'] = getWeiboPage.body['page']-1
        url = url +urllib.urlencode(getWeiboPage.body)
        try: 
            req = urllib2.Request(url)
            result = urllib2.urlopen(req)
            text = result.read()
        except Exception: 
            return
        #content = eval("u'''"+text+"'''").encode(getWeiboPage.charset)
        content = eval("u\"\"\" "+text+"\n \"\"\" ").encode(getWeiboPage.charset)
        #self.writefile('C:/weibodata/'+self.uid+'/text'+str(getWeiboPage.body['page'])+'_1.html',text)
        pattern = re.compile('<script>STK && STK.pageletM && STK.pageletM.view\((.*?)\)<\/script>')
        result = pattern.findall(text)
        jsonResult = json.loads(result[8])
        soup = BeautifulSoup(jsonResult['html'])
        resultes = soup('div','WB_feed')
        feedlist=resultes[0].findAll('div',attrs={'class': "WB_feed_type SW_fun "})
        for feed in feedlist:
            try:
                isforward='isforward:'+feed['isforward']+'  '
                forward=1
            except Exception as e:
                forward=0
                isforward='isforward:0  '
            
            mid='mid:'+feed['mid']+'  '
            source=feed.findAll('div',attrs={'class': "WB_from"})
            if forward:
                try:
                    a=source[1].findAll('a')
                except Exception as e:
                    a=source[0].findAll('a')
            else:
                a=source[0].findAll('a')
            ct='ct:'+a[0]['date']+'  '
            srn='srn:'+a[1].text+'  '
            
            text=feed.findAll('div',attrs={'class': "WB_text"})
            WB_text='WB_text:'+text[0].text+'   \n'
            
            self.writefile(self.path+'/'+self.uid+'_profile.txt',mid)
            self.writefile(self.path+'/'+self.uid+'_profile.txt',ct)
            self.writefile(self.path+'/'+self.uid+'_profile.txt',srn)
            self.writefile(self.path+'/'+self.uid+'_profile.txt',isforward)
            self.writefile(self.path+'/'+self.uid+'_profile.txt',WB_text)
        #self.writefile('C:/weibodata/'+self.uid+'/transText'+str(getWeiboPage.body['page'])+'_1.html',str(resultes[0]))
        
        if getWeiboPage.flag == 0:
            self.get_totallPageNum(content)
            getWeiboPage.flag = 1
        #self.get_content(text)
    def get_secondpage(self,url):
        getWeiboPage.body['count'] = '15'
    #   getWeiboPage.body['end_id'] = '3490160379905732'
    #   getWeiboPage.body['max_id'] = '3487344294660278'
        getWeiboPage.body['pagebar'] = '0'
        getWeiboPage.body['pre_page'] = getWeiboPage.body['page']

        url = url +urllib.urlencode(getWeiboPage.body)
        try: 
            req = urllib2.Request(url)
            result = urllib2.urlopen(req)
            text = result.read()
        except Exception: 
            return
        
        #content = eval("u'''"+text+"'''").encode(getWeiboPage.charset)
        content = eval("u\"\"\" "+text+"\n \"\"\" ").encode(getWeiboPage.charset)
        
        pattern = re.compile('<script>STK && STK.pageletM && STK.pageletM.view\((.*?)\)<\/script>')
        result = pattern.findall(text)
        jsonResult = json.loads(result[8])
        soup = BeautifulSoup(jsonResult['html'])
        resultes = soup('div','WB_feed')
        feedlist=resultes[0].findAll('div',attrs={'class': "WB_feed_type SW_fun "})
        for feed in feedlist:
            try:
                isforward='isforward:'+feed['isforward']+'  '
                forward=1
            except Exception as e:
                forward=0
                isforward='isforward:0  '
                    
            mid='mid:'+feed['mid']+'  '
            source=feed.findAll('div',attrs={'class': "WB_from"})
            if forward:
                try:
                    a=source[1].findAll('a')
                except Exception as e:
                    a=source[0].findAll('a')
            else:
                a=source[0].findAll('a')
            ct='ct:'+a[0]['date']+'  '
            srn='srn:'+a[1].text+'  '
                    
            text=feed.findAll('div',attrs={'class': "WB_text"})
            WB_text='WB_text:'+text[0].text+'   \n'
                    
            self.writefile(self.path+'/'+self.uid+'_profile.txt',mid)
            self.writefile(self.path+'/'+self.uid+'_profile.txt',ct)
            self.writefile(self.path+'/'+self.uid+'_profile.txt',srn)
            self.writefile(self.path+'/'+self.uid+'_profile.txt',isforward)
            self.writefile(self.path+'/'+self.uid+'_profile.txt',WB_text)
           
        
        
    def get_thirdpage(self,url):
        getWeiboPage.body['count'] = '15'
        getWeiboPage.body['pagebar'] = '1'
        getWeiboPage.body['pre_page'] = getWeiboPage.body['page']

        url = url +urllib.urlencode(getWeiboPage.body)
        try: 
            req = urllib2.Request(url)
            result = urllib2.urlopen(req)
            text = result.read()
        except Exception: 
            return
        
        #content = eval("u'''"+text+"'''").encode(getWeiboPage.charset)
        content = eval("u\"\"\" "+text+"\n \"\"\" ").encode(getWeiboPage.charset)
        pattern = re.compile('<script>STK && STK.pageletM && STK.pageletM.view\((.*?)\)<\/script>')
        result = pattern.findall(text)
        jsonResult = json.loads(result[8])
        soup = BeautifulSoup(jsonResult['html'])
        resultes = soup('div','WB_feed')
        feedlist=resultes[0].findAll('div',attrs={'class': "WB_feed_type SW_fun "})
        for feed in feedlist:
            try:
                isforward='isforward:'+feed['isforward']+'  '
                forward=1
            except Exception as e:
                forward=0
                isforward='isforward:0  '
                            
            mid='mid:'+feed['mid']+'  '
            source=feed.findAll('div',attrs={'class': "WB_from"})
            if forward:
                try:
                    a=source[1].findAll('a')
                except Exception as e:
                    a=source[0].findAll('a')
            else:
                a=source[0].findAll('a')
            ct='ct:'+a[0]['date']+'  '
            srn='srn:'+a[1].text+'  '
                            
            text=feed.findAll('div',attrs={'class': "WB_text"})
            WB_text='WB_text:'+text[0].text+'   \n'
                            
            self.writefile(self.path+'/'+self.uid+'_profile.txt',mid)
            self.writefile(self.path+'/'+self.uid+'_profile.txt',ct)
            self.writefile(self.path+'/'+self.uid+'_profile.txt',srn)
            self.writefile(self.path+'/'+self.uid+'_profile.txt',isforward)
            self.writefile(self.path+'/'+self.uid+'_profile.txt',WB_text)
            
        
        
    def get_url(self,uid):
        url = 'http://weibo.com/' + uid + '?from=otherprofile&wvr=3.6&loc=tagweibo'
        return url
    def get_uid(self,filename):
        fread = file(filename)
        for line in fread:
            getWeiboPage.uid_list.append(line)
            print line
            time.sleep(1)
    def writefile(self,filename,content):
        fw = file(filename,'a')
        fw.write(content)
        fw.close()
    def get_content(self,text):
        p = re.compile('<[^>]+>')
        #print p.sub("",text)
        self.writefile('C:/weibodata/'+self.uid+'/content'+str(getWeiboPage.body['page'])+'_3',p.sub("",text))
