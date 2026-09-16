from common import MySQLUtil
def query_history_menu(username):
    conn = MySQLUtil.get_mysql_conn()
    cursor = conn.cursor()
    sql = "SELECT history_id, question, create_time FROM history WHERE username=%s AND parent_id=0"
    cursor.execute(sql, [username])
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
def conversation_log(historyId):
    conn = MySQLUtil.get_mysql_conn()
    cursor = conn.cursor()
    sql = "SELECT question, answer, history_id,summary FROM history WHERE history_id=%s or parent_id=%s  ORDER BY history_id ASC;"
    cursor.execute(sql, [historyId, historyId])
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
def conversation_delete(historyId):
    conn = MySQLUtil.get_mysql_conn()
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM history WHERE history_id=%s or parent_id=%s;"
        cursor.execute(sql, [historyId, historyId])
        # 联动删除该会话的摘要记录（history_summary.history_id 存的是会话锚点 id），避免孤儿数据
        sql2 = "DELETE FROM history_summary WHERE history_id=%s;"
        cursor.execute(sql2, [historyId])
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
    return 1

def update_summary(historyId, summary):
    conn = MySQLUtil.get_mysql_conn()
    cursor = conn.cursor()
    try:
        sql = "UPDATE history SET summary=%s WHERE history_id=%s;"
        cursor.execute(sql, [summary, historyId])
        conn.commit()
        cursor.close()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
