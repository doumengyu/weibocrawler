#!/usr/bin/env python
# -*- coding: utf-8 -*-

import weiboLogin
import search
import getUserInfo
import urllib
import urllib2
import os
import sys

from WeiboEntity import WeiboEntity
from UserEntity import UserEntity
reload(sys)
sys.setdefaultencoding('utf-8')

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
    keyword = '和田玉'
    SerachPage=search.Search()
    SerachPage.get_user(keyword)
    weibo_list = SerachPage.weibo_list
    UserInfo = getUserInfo.GetUserInfo()
    user_list = []
    for weibo in weibo_list:
        print weibo.uid
        UserInfo.get_userinfo(weibo.uid)
        user = UserInfo.user
        user_list.append(user)
    user_list_final = []
    for user in user_list: 
        if user.isverified == 1:
            user_list_final.append(user)
            user_list.remove(user)   
    user_list.sort(lambda p1,p2:cmp(p1.fansnumber,p2.fansnumber),reverse=True)
    for user in user_list:
        user_list_final.append(user)
    for user1 in user_list_final:
        print user1.fansnumber

    


