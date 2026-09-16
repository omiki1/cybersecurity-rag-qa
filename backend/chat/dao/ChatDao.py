from common import MySQLUtil

def save_conversation_result(question: str, username: str, parent_id: int, answer: str):
    conn = MySQLUtil.get_mysql_conn()
    cursor = conn.cursor()
    try:
        sql = "insert into history (question, username, parent_id, answer, create_time) values (%s,%s,%s,%s, now());"
        cursor.execute(sql,(question,username,parent_id,answer))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
# def updata_summary_history(historyId: int,):
#     conn = MySQLUtil.get_mysql_conn()
#     cursor = conn.cursor()
#     try:
#         sql = "updata into history values (null,%s,%s,%s,now());"

# def is_summary(hitorty_id):
