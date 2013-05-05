#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib
import urllib2
import cookielib
import base64
import re
import json
import hashlib

class weiboLogin:
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'ssosimplelogin': '1',
        'vsnf': '1',
        'vsnval': '',
        'su': '',
        'service': 'miniblog',
        'servertime': '',
        'nonce': '',
        'pwencode': 'wsse',
        'sp': '',
        'encoding': 'UTF-8',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }

    def get_servertime(self):
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=dW5kZWZpbmVk&client=ssologin.js(v1.3.18)&_=1329806375939'
        data = urllib2.urlopen(url).read()
        p = re.compile('\((.*)\)')
        try:
            json_data = p.search(data).group(1)
            data = json.loads(json_data)
            servertime = str(data['servertime'])
            nonce = data['nonce']
            return servertime, nonce
        except:
            print 'Get severtime error!'
            return None

    def get_pwd(self, pwd, servertime, nonce):
        pwd1 = hashlib.sha1(pwd).hexdigest()
        pwd2 = hashlib.sha1(pwd1).hexdigest()
        pwd3_ = pwd2 + servertime + nonce
        pwd3 = hashlib.sha1(pwd3_).hexdigest()
        return pwd3

    def get_user(self, username):
        username_ = urllib.quote(username)
        username = base64.encodestring(username_)[:-1]
        return username


    def login(self,username,pwd):
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.18)'
        try:
            servertime, nonce = self.get_servertime()
        except:
            print 'get servertime error!'
            return 'servertime_error'
        weiboLogin.postdata['servertime'] = servertime
        weiboLogin.postdata['nonce'] = nonce
        weiboLogin.postdata['su'] = self.get_user(username)
        weiboLogin.postdata['sp'] = self.get_pwd(pwd, servertime, nonce)
        weiboLogin.postdata = urllib.urlencode(weiboLogin.postdata)
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0 Chrome/20.0.1132.57 Safari/536.11'}
        req  = urllib2.Request(
            url = url,
            data = weiboLogin.postdata,
            headers = headers
        )
        result = urllib2.urlopen(req)
        text = result.read()
        p = re.compile('location\.replace\(\'(.*?)\'\)')
        try:
            login_url = p.search(text).group(1)
            urllib2.urlopen(login_url)
            print "Login success!"
        except:
            print 'Login error!'
