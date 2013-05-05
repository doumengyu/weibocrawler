#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo import APIError, APIClient

import weiboconfig as config
import os, logging
import random
import httplib
import urllib
import urlparse



class Client:
    _instalce = ''
    _init = 0
    @classmethod  
    def instance(cls):  
        if not cls._instalce:  
            cls._instalce = cls()
        return cls._instalce 
    
    def init(self):
        #定义供替换的APP Key和Secret
        APP_KEYS_SECRETS=config.APP_KEYS_SECRETS
        self.length = len(APP_KEYS_SECRETS)
        current_index = int(random.random()*100 % self.length) 
        self.client=self.access_client(current_index)
        self._init=1
    def access_client(self,app_index):
        #定义供替换的APP Key和Secret
        APP_KEYS_SECRETS=config.APP_KEYS_SECRETS
        
        ##随机取出一个app index
        #current_index = int(random.random()*100 % len(APP_KEYS_SECRETS))    
        APP_KEY=  APP_KEYS_SECRETS[app_index][0] #app key
        APP_SECRET = APP_KEYS_SECRETS[app_index][1] # app secret
        CALLBACK_URL = config.CALLBACK_URI # callback url
        username=config.ACCOUNT1
        password=config.PASSWORD1
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        url = client.get_authorize_url()
        conn = httplib.HTTPSConnection('api.weibo.com')
        postdata = urllib.urlencode({'client_id':APP_KEY,'response_type':'code','redirect_uri':CALLBACK_URL,'action':'submit','userId':username,'passwd':password,'isLoginSina':0,'from':'','regCallback':'','state':'','ticket':'','withOfficalFlag':0})
        conn.request('POST','/oauth2/authorize',postdata,{'Referer':url, 'Content-Type': 'application/x-www-form-urlencoded'})
        res = conn.getresponse()
        page = res.read()
        conn.close()##拿新浪给的code
        code = urlparse.parse_qs(urlparse.urlparse(res.msg['location']).query)['code'][0]
        token = client.request_access_token(code)
        access_token = token.access_token # 新浪返回的token，类似abc123xyz456
        expires_in = token.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
        # TODO: 在此可保存access token
        client.set_access_token(access_token, expires_in)##生成token
        return client
        
    #获取用户信息
    def get_users_show(self,uid):
        try:
            return self.client.users.show.get(uid=uid)
        except Exception ,e:
            current_index = int(random.random()*100 % self.length) 
            self.client=self.access_client(current_index)
            return self.get_users_show(uid)
        
    
    #获取用户所发布的微博
    def get_statuses_user_timeline(self,uid,count=20,page=1):
        try:
            return self.client.statuses.user_timeline.get(uid=uid,count=count,page=page)
        except Exception ,e:
            current_index = int(random.random()*100 % self.length) 
            self.client=self.access_client(current_index)
            return self.get_statuses_user_timeline(uid,count,page)
        
    #获取用户所发布的微博总数目
    def get_user_counts(self,uid):
        try:
            return self.client.users.counts.get(uids=uid)
        except Exception ,e:
            current_index = int(random.random()*100 % self.length) 
            self.client=self.access_client(current_index)
            return self.get_user_counts(uid)
        
    #获取用户所发布的微博总数目
    def get_friendids(self,uid):
        try:
            return self.client.friendships.friends.ids.get(uid=uid,count=3000)
        except Exception ,e:
            current_index = int(random.random()*100 % self.length) 
            self.client=self.access_client(current_index)
            return self.get_friendids(uid=uid,count=3000)
    
    
    
        


def writefile(filename,content):
    fw = file(filename,'a')
    fw.write(content)
    fw.close()


            
if __name__=='__main__':
     writefile('C:/info1.txt',str(get_users_show('1670662622')))
      
        
    
    
    