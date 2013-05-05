# -*- coding: UTF-8 -*- 
# Create your views here.


import weiboconfig as config
import client
import mysqlconn

if __name__=='__main__':
    #connect to the mysql db
    conn = mysqlconn.dbconn()
   
    
    Client = client.Client.instance()
    if Client._init ==0:
       Client.init()
    statuses_count = Client.get_statuses_user_timeline('1710173801').total_number;
    count = 100
    page_count =  statuses_count/count+1
    print page_count
    for i in range(1, page_count+1):   
        statuses = Client.get_statuses_user_timeline('1710173801',count,i).statuses
        for status in statuses:
            try:
                cursor = conn.cursor()
                insertstring = 'insert ignore into oppo_weibo (mid,text,source,reposts_count,comments_count,attitudes_count,id,created_at) values ('+'\''+str(status.mid)+'\''+','+'\''+status.text+'\''+','+'\''+status.source+'\''+','+str(status.reposts_count)+','+str(status.comments_count)+','+str(status.attitudes_count)+','+'\''+str(status.id)+'\''+','+'\''+status.created_at+'\''+')'
                cursor.execute(insertstring)
                #close the cursor
                cursor.close()
                conn.commit()
            except Exception:
                pass
    #disconnet the link to mysql db
    mysqlconn.dbclose(conn)
        
    
    