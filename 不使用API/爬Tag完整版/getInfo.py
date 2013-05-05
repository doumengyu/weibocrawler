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
import time,datetime
from bs4 import BeautifulSoup


socket.setdefaulttimeout(60)

reload(sys)
sys.setdefaultencoding('utf-8')


class getInfo:
    uid_list = []
    charset = 'utf8'
    uid = '';
    path='C:/weibodata'
    
    
    def get_info(self,uid):
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='weibo',port=3306,charset='utf8')
        self.uid = uid
        url = self.get_url(uid)
        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
        text = result.read()
        pattern = re.compile('<script>STK && STK.pageletM && STK.pageletM.view\((.*?)\)<\/script>')
        result = pattern.findall(text)
        jsonResult1 = json.loads(result[8])   #获取基本信息和联系信息
        jsonResult4=json.loads(result[11])    #获取Tag信息
        
        soup1 = BeautifulSoup(jsonResult1['html'])
        soup4 = BeautifulSoup(jsonResult4['html'])
        
        resultes1 = soup1.findAll('div',attrs={'class': "pf_item clearfix"})
        screenname=''
        truename=''
        address=''
        sex=''
        birthday=''
        blood=''
        blog=''
        domain=''
        description=''
        mail=''
        QQ=''
        MSN=''
        if resultes1 is not None:
            for result in resultes1:
                try:
                    label=result.find('div',attrs={'class': "label S_txt2"}).text
                    info=result.find('div',attrs={'class': "con"}).text
                    if label=='昵称':
                        screenname=info.strip()
                    else:
                        if label=='真实姓名':
                            truename=info.strip()
                        else:
                            if label=='所在地':
                                address=info.strip()
                            else:
                                if label=='性别':
                                    sex=info.strip()
                                else:
                                    if label=='生日':
                                        birthday=info.strip()
                                    else:
                                        if label=='血型':
                                            blood=info.strip()
                                        else:
                                            if label=='博客':
                                                blog=info.strip()
                                            else:
                                                if label=='个性域名':
                                                    domain=info.strip()
                                                else:
                                                    if label=='简介':
                                                        description=info.strip()
                                                    else:
                                                        if label=='邮箱':
                                                            mail=info.strip()
                                                        else:
                                                            if label=='QQ':
                                                                QQ=info.strip()
                                                            else:
                                                                if label=='MSN':
                                                                    MSN=info.strip()
                except Exception as e:
                    pass
        
        try:
            #conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='weibo',port=3306,charset='utf8')
            cur = conn.cursor()
            d = datetime.datetime.strptime(birthday,"%Y年%m月%d日")
            #birthdaystring = 'update user set birthday='+'\''+birthday+'\''+' where id='+'\''+self.uid+'\''
            birthdaystring = 'update user set birthday='+'\''+str(d.year)+'\''+' where id='+'\''+self.uid+'\''
            cur.execute(birthdaystring)
            conn.commit()
            cur.close()
            #conn.close()
        except Exception as e:
            pass
        
        
       
        
        resultes4 = soup4.findAll('div',attrs={'class': "pf_item clearfix"})
        taglist=[]
        if resultes4 is not None:
            for result in resultes4:
                try:
                    tags=result.find('div',attrs={'class': "con"})
                    tag_as=tags.findAll('a')
                    for tag_a in tag_as:
                        taginfo=tag_a.text
                        taglist.append(taginfo)
                    
                except Exception as e:
                    pass
        for tagfinal in taglist:
            try:
                #conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='weibo',port=3306,charset='utf8')
                cur = conn.cursor()
                tagstring = 'insert ignore into user_tag (uid,tag) values ('+'\''+self.uid+'\''+','+'\''+tagfinal+'\''+')'
                cur.execute(tagstring)
                conn.commit()
                cur.close()
                #conn.close()
            except Exception as e:
                pass
            
        conn.close()
    def get_url(self,uid):
         url = 'http://weibo.com/' + uid + '/info?from=profile&wvr=5&loc=tabinf#profile_tab'
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
    
