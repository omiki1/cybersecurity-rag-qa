from common import MySQLUtil

def update_summary(history_id,username,summary):
    conn  = None
    cursor = None
    try:
        conn = MySQLUtil.get_mysql_conn()
        cursor = conn.cursor()
        sql = 'insert into history_summary (history_id,username,summary) values (%s,%s,%s);'
        cursor.execute(sql,(history_id,username,summary))
        conn.commit()
        cursor.close()
        conn.close()
        return 1
    except Exception as e:
        conn.rollback()
        print(e)
        return 0

def get_summary(history_id,username):
    conn = None
    cursor = None
    try:
        conn = MySQLUtil.get_mysql_conn()
        cursor = conn.cursor()
        sql = 'Select summary from history_summary where history_id = %s and username = %s;'
        cursor.execute(sql, (history_id, username))
        data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return {
            'data': data,
        }
    except Exception as e:
        conn.rollback()
        print(e)

