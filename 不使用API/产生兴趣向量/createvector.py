#! /usr/bin/env python
#coding=utf-8
import os
import sys
import MySQLdb
import time

reload(sys)
sys.setdefaultencoding('utf-8')


def get_uid(filename,uid_list):
    fread = file(filename)
    for line in fread:
        uid_list.append(line.strip())

def writefile(filename,content):
    fw = file(filename,'a')
    fw.write(content)
    fw.close()
        

if __name__ == '__main__':
    uid_list=[]
    get_uid('C:/Result1.txt',uid_list)
    for uid in uid_list:
        follow_list = []
        vector = {'10':0,'11':0,'12':0,'13':0,'14':0,'15':0,'16':0,'17':0,'18':0,'19':0,'20':0}
        try:
            path='C:/weibodata/'+uid+'_follow.txt'
            get_uid(path,follow_list)
        except Exception as e:
            writefile('C:/id.txt',str(uid)+'\n')
        conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='weibo',port=3306,charset='utf8')
        for follow in follow_list:
            cur = conn.cursor()
            selectstring = 'select cid from user_category_selected where uid = '+'\''+follow+'\''
            count = cur.execute(selectstring)
            print count
            result = cur.fetchone()
            if count == 1:
                category = result[0]
                vector[category] = vector[category]+1
            cur.close()
           
        cur = conn.cursor()
        vectorstring = 'insert ignore into user_vector (uid,entertainment,fashion,literature,it,sports,games,finance,qualitylife,shoppingonline,science,service) values ('+'\''+uid+'\''+','+str(vector['10'])+','+str(vector['11'])+','+str(vector['12'])+','+str(vector['13'])+','+str(vector['14'])+','+str(vector['15'])+','+str(vector['16'])+','+str(vector['17'])+','+str(vector['18'])+','+str(vector['19'])+','+str(vector['20'])+')'
        cur.execute(vectorstring)
        conn.commit()
        cur.close()
        conn.close()       
    
