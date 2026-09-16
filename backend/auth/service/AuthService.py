import time

from common import RedisUtil
from common.JWTUtil import create_access_token
from common.HashPwdUtil import verify_password
from user.dao import UsersDao

def password_login(login_entity):
    result = UsersDao.check_email(login_entity.email)
    if not result:
        return {
            'code': 500,
            'msg': '邮箱不存在',
            'data': None
        }
    else:
        user_password = result[0]['password_hash']
        if verify_password(login_entity.password, user_password):
            return {
                'code': 200,
                'msg': '登录成功',
                'data': create_access_token({
                    'user_id': result[0]['users_id'],
                    'username': result[0]['username'],
                    'role_name': result[0]['role_name'],
                })
            }
        else:

            return {
                'code': 500,
                'msg': f'密码错误',
                'data': None,
            }
def login_by_code(login_entity):
    r = None
    try:
        r = RedisUtil.get_redis_conn()
        stored = r.get(login_entity.email)
        if stored is None:
            return {'code': 500, 'msg': '验证码已过期或未发送', 'data': None}
        if stored.decode() != login_entity.code:
            return {'code': 500, 'msg': '验证码错误', 'data': None}
        r.delete(login_entity.email)
        result = UsersDao.check_email(login_entity.email)
        if not result:
            return {'code': 500, 'msg': '邮箱不存在', 'data': None}
        return {
            'code': 200,
            'msg': '登录成功',
            'data': create_access_token({
                'user_id': result[0]['users_id'],
                'username': result[0]['username'],
                'role_name': result[0]['role_name'],
            }),
        }
    except Exception as e:
        print(e)
        return {'code': 500, 'msg': f'验证码登录失败: {e}', 'data': None}
    finally:
        if r:
            RedisUtil.close_redis_conn(r)

def guest_login():
    """游客登录"""
    return {
        'code': 200,
        'msg': '游客登录成功',
        'data': create_access_token({
            'user_id': 0,
            'username': 'guest',
            'role_name': 'guest',
        }),
    }


def logout(user):
    jti = user.get("jti")
    expires = user.get("exp")
    if jti and expires:
        remain = expires - time.time()
        if remain > 0:
            r = RedisUtil.get_redis_conn()
            r.set(f"blacklist:{jti}", 1, ex=max(int(remain), 1))
            RedisUtil.close_redis_conn(r)
    return {'code': 200, 'msg': '已退出登录', 'data': None}

