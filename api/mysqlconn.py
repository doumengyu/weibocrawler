import MySQLdb

def dbconn():
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', db='weibo', port=3306, charset='utf8')
    return conn

def dbclose(conn):
    conn.close()



