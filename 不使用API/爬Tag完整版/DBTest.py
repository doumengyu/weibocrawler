#! /usr/bin/env python
#coding=utf-8

import MySQLdb

if __name__ == '__main__':
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='weibo',port=3306)
        cur=conn.cursor()
        count=cur.execute('select * from user_info')
        print 'there has %s rows record' % count
         
        result=cur.fetchone()
        print result
     
        results=cur.fetchmany(5)
        for r in results:
            print r
        
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    