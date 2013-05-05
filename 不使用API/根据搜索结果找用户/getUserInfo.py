#! /usr/bin/env python
#coding=utf-8


import urllib
import urllib2
import sys
import time
import re
import socket
import json
import MySQLdb
from UserEntity import UserEntity
from bs4 import BeautifulSoup


socket.setdefaulttimeout(60)

reload(sys)
sys.setdefaultencoding('utf-8')


class GetUserInfo:
    user = None
    def get_userinfo(self,uid):
        self.user = UserEntity()
        self.user.uid=uid
        url = self.get_url(uid)
        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
        text = result.read()
        content = eval("u\"\"\" "+text+"\n \"\"\" ").encode('utf-8')
        self.user.followersnumber=self.get_followersnum(content)
        self.user.fansnumber=self.get_fansnum(content)
        self.user.messagesnumber=self.get_messagesnum(content)
        pattern = re.compile('<script>STK && STK.pageletM && STK.pageletM.view\((.*?)\)<\/script>')
        result = pattern.findall(text)
        extraResult = json.loads(result[3])  #获取认证信息或达人信息
        extraString = extraResult['html']
        verified = 'http://img.t.sinajs.cn/t5/style/images/index/ico_sinaVIP.png'
        daren = 'http://img.t.sinajs.cn/t5/style/images/index/club.png'
        if str(extraString).find(verified):
            self.user.isverified = 1
        if str(extraString).find(daren):
            self. user.isdaren = 1
        
        jsonResult = json.loads(result[8])   #获取基本信息和联系信息
        soup = BeautifulSoup(jsonResult['html'])
        results = soup.findAll('div',attrs={'class': "pf_item clearfix"})
        if results is not None:
            for result in results:
                try:
                    label=result.find('div',attrs={'class': "label S_txt2"}).text
                    info=result.find('div',attrs={'class': "con"}).text
                    if label=='昵称':
                        user.screenname=info.strip()
                    else:
                        if label=='所在地':
                            self.user.address=info.strip()
                        else:
                            if label=='性别':
                                self.user.sex=info.strip()
                            else:
                                if label=='简介':
                                    self.user.description=info.strip()
                                else:
                                   if label=='生日':
                                       self.user.birthday=info.strip()
                                
                except Exception as e:
                    pass
    
    def get_url(self,uid):
        url = 'http://weibo.com/' + uid + '/info?from=profile&wvr=5&loc=tabinf#profile_tab'
        return url
    def get_fansnum(self,content):
        tag1 = '<strong node-type=\"fans\">'
        pos1 = content.find(tag1)+len(tag1)
        tag2 = '<\/strong>'
        pos2 = content.find(tag2,pos1)
        return int(float(content[pos1:pos2]))
    
    def get_followersnum(self,content):
        tag1 = '<strong node-type=\"follow\">'
        pos1 = content.find(tag1)+len(tag1)
        tag2 = '<\/strong>'
        pos2 = content.find(tag2,pos1)
        return int(float(content[pos1:pos2]))

    def get_messagesnum(self,content):
        tag1 = '<strong node-type=\"weibo\">'
        pos1 = content.find(tag1)+len(tag1)
        tag2 = '<\/strong>'
        pos2 = content.find(tag2,pos1)
        return int(float(content[pos1:pos2]))
    
    
        
        
        