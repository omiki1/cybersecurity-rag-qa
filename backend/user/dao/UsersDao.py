from common import MySQLUtil
from common.HashPwdUtil import crypt


def check_email(email):
    conn = cur = None
    try:
        conn = MySQLUtil.get_mysql_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        return cur.fetchall()
    except Exception as e:
        print(f'数据库查询失败: {e}')
        return None
    finally:
        cur.close()
        conn.close()

def get_user_profile(email):
    """资料查询"""
    conn = cur = None
    try:
        conn = MySQLUtil.get_mysql_conn()
        cur = conn.cursor()
        cur.execute("SELECT email, username, role_name FROM users WHERE email = %s LIMIT 1", [email])
        return cur.fetchone()
    except Exception as e:
        print(f'用户资料查询失败: {e}')
        return None
    finally:
        if cur: cur.close()
        if conn: conn.close()

def add_user(username, email, password):
    conn = cur = None
    try:
        conn = MySQLUtil.get_mysql_conn()
        cur = conn.cursor()
        password_hash = crypt.hash(password)
        sql = "INSERT INTO users (username, email, password_hash, role_name) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, [username, email, password_hash, 'user'])   # 角色后端硬编码 user，不由前端传
        conn.commit()
        return {'code': 200, 'msg': '注册成功', 'data': None}
    except Exception as e:
        print(f'注册失败{e}')
        return {
            'code': 400,
            'msg': f'注册失败{e}',
            'data': None,
        }
    finally:
        cur.close()
        conn.close()


