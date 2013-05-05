#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import sys
import time
import re
import socket
import json
import html5lib
import MySQLdb
from WeiboEntity import WeiboEntity
from bs4 import BeautifulSoup

socket.setdefaulttimeout(60)

reload(sys)
sys.setdefaultencoding('utf-8')


class Search:
    weibo_list = []
    def get_user(self,keyword,page = 1):
        url = self.get_url(keyword)
        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
        text = result.read()
        pattern = re.compile('<script>STK && STK.pageletM && STK.pageletM.view\((.*?)\)<\/script>')
        result = pattern.findall(text)
        jsonResult = json.loads(result[8])
        soup = BeautifulSoup(jsonResult['html'])
        dls = soup.findAll('dl',attrs={'class': "feed_list",'action-type' : "feed_list_item"})
        for dl in dls:
            weibo = WeiboEntity()
            weibo.mid = dl['mid']
            try:
                weibo.isForward = dl['isforward']
            except Exception as e:
                weibo.isForward = '0'
            p_content = dl.find('p',attrs={'node-type': "feed_list_content"})
            a_usercard = p_content.find('a',attrs={'target': "_blank"})
            usercard = a_usercard['usercard'].strip().split('&')[0]
            weibo.uid = usercard[3:]
            em_text = p_content.find('em')
            weibo.text = em_text.text.strip()
            if '1' == weibo.isForward:
                try:
                    dt_forward = dl.find('dt',attrs={'node-type': "feed_list_forwardContent"})
                    em_forwardtext = dt_forward.find('em')
                    weibo.sourcetext = em_forwardtext.text.strip()
                except Exception as e:
                    pass
            p_info = dl.find('p',attrs={'class': "info W_linkb W_textb"})
            a_time = p_info.find('a',attrs={'class': "date",'node-type': "feed_list_item_date"})
            weibo.createtime = a_time['date']
            a_source = p_info.find('a',attrs={'target': "_blank"})
            weibo.source = a_source.text
            span_count = p_info.find('span')
            a_forwardcount = span_count.find('a',attrs={'action-type': "feed_list_forward"})
            a_commentcount = span_count.find('a',attrs={'action-type': "feed_list_comment"})
            if a_forwardcount.text.strip() == '转发':
                weibo.forwardcount = 0
            else:
                text_forward = a_forwardcount.text.strip()
                begin = text_forward.index('(')+1
                end = text_forward.index(')')
                forwardcount = text_forward[begin:end]
                weibo.forwardcount = int(forwardcount)
            if a_commentcount.text.strip() == '评论':
                weibo.commentcount = 0
            else:
                text_comment = a_commentcount.text.strip()
                begin = text_comment.index('(')+1
                end = text_comment.index(')')
                commentcount = text_comment[begin:end]
                weibo.commentcount = int(commentcount)
            self.weibo_list.append(weibo)
        #if page == 1:
        #    pagecount = 1
        #    div_pagecount = soup.find('div',attrs={'class': "search_page clearfix"})
        #    lis = div_pagecount.findAll('li')
        #    for li in lis:
        #       if li.text.strip() == '下一页' or li.text.strip() == '...':
        #            pass
        #       else:
        #            if pagecount < int(li.text.strip()):
        #                pagecount = int(li.text.strip())
        #    i = 2
        #    while i<=pagecount and i<=2:
        #        self.get_user(keyword,page = i)
        #        i = i+1
        
        
    def get_url(self,keyword,page = 1):
        url = 'http://s.weibo.com/weibo/' + keyword + '&page=' + str(page)
        return url
    
    def writefile(self,filename,content):
        fw = file(filename,'a')
        fw.write(content)
        fw.close()
    
    