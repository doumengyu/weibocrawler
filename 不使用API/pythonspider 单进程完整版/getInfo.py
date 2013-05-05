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


class getInfo:
    uid_list = []
    charset = 'utf8'
    uid = '';
    path='C:/weibodata'
    
    
    def get_info(self,uid):
        self.uid = uid
        url = self.get_url(uid)
        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
        text = result.read()
        pattern = re.compile('<script>STK && STK.pageletM && STK.pageletM.view\((.*?)\)<\/script>')
        result = pattern.findall(text)
        jsonResult1 = json.loads(result[8])   #获取基本信息和联系信息
        jsonResult2=json.loads(result[9])     #获取工作信息
        jsonResult3=json.loads(result[10])    #获取教育信息
        jsonResult4=json.loads(result[11])    #获取Tag信息
        
        soup1 = BeautifulSoup(jsonResult1['html'])
        soup2 = BeautifulSoup(jsonResult2['html'])
        soup3 = BeautifulSoup(jsonResult3['html'])
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
        self.writefile(self.path+'/'+self.uid+'_info.txt','screenname:'+screenname+'\n')
        self.writefile(self.path+'/'+self.uid+'_info.txt','truename:'+truename+'\n')
        self.writefile(self.path+'/'+self.uid+'_info.txt','address:'+address+'\n')
        self.writefile(self.path+'/'+self.uid+'_info.txt','sex:'+sex+'\n')
        self.writefile(self.path+'/'+self.uid+'_info.txt','birthday:'+birthday+'\n')
        self.writefile(self.path+'/'+self.uid+'_info.txt','blood:'+blood+'\n')
        self.writefile(self.path+'/'+self.uid+'_info.txt','blog:'+blog+'\n')
        self.writefile(self.path+'/'+self.uid+'_info.txt','domain:'+domain+'\n')
        self.writefile(self.path+'/'+self.uid+'_info.txt','description:'+description+'\n')
        self.writefile(self.path+'/'+self.uid+'_info.txt','mail:'+mail+'\n')
        self.writefile(self.path+'/'+self.uid+'_info.txt','domain:'+domain+'\n')
        self.writefile(self.path+'/'+self.uid+'_info.txt','MSN:'+MSN+'\n')
        
        
        resultes2 = soup2.findAll('div',attrs={'class': "pf_item clearfix"})
        careerlist=[]
        if resultes2 is not None:
            for result in resultes2:
                try:
                    careers=result.findAll('div',attrs={'class': "con"})
                    for career in careers:
                        career_a=career.find('a')
                        careerinfo=career_a.text
                        careerlist.append(careerinfo)
                except Exception as e:
                    pass
                
        for careerfinal in careerlist:
            self.writefile(self.path+'/'+self.uid+'_info.txt','career:'+careerfinal+'\n')
            
        resultes3 = soup3.findAll('div',attrs={'class': "pf_item clearfix"})
        educationlist=[]
        if resultes3 is not None:
            for result in resultes3:
                try:
                    educations=result.findAll('div',attrs={'class': "con"})
                    for education in educations:
                        education_a=education.find('a')
                        educationinfo=education_a.text
                        educationlist.append(educationinfo)
                except Exception as e:
                    pass
        for educationfinal in educationlist:
            self.writefile(self.path+'/'+self.uid+'_info.txt','education:'+educationfinal+'\n')
        
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
            self.writefile(self.path+'/'+self.uid+'_info.txt','tag:'+tagfinal+'\n')
                
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
    