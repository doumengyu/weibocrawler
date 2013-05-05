import client
import mysqlconn

if __name__=='__main__':
    #connect to the mysql db
    conn = mysqlconn.dbconn()
   
    
    Client = client.Client.instance()
    if Client._init ==0:
       Client.init()
    ids = Client.get_friendids('1710173801').ids;
    
    try:
        for id in ids:
            cursor = conn.cursor()
            insertstring = 'insert ignore into oppo_follow (uid,follow_id) values ( \'1710173801\','+'\''+str(id)+'\''+')'
            cursor.execute(insertstring)
            #close the cursor
            cursor.close()
            conn.commit()
            
        
    except Exception:
        pass
    
    
    
    #disconnet the link to mysql db
    mysqlconn.dbclose(conn)
