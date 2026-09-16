import os
import smtplib
from email.mime.text import MIMEText
from random import random
from dotenv import load_dotenv

from common import RedisUtil
from common.HashPwdUtil import hash_password
from user.dao import UsersDao

def get_profile(email):
    profile = UsersDao.get_user_profile(email)
    if profile is None:
        return None
    else:
        return {
            'code':200,
            'msg':'查询成功',
            'data':profile
        }
def send_email(email):
    """给已注册邮箱发送 4 位验证码，存 Redis 60s"""
    result = UsersDao.check_email(email)
    if not result:                      # 邮箱不存在不发码
        return {
            'code':400,
            'msg':'邮箱不存在',
            'data':None
        }

    username = result[0]['username']
    code = ''.join(str(int(random() * 10)) for _ in range(4))   # 4 位随机码

    sender = os.getenv('SENDER_EMAIL')
    sender_pwd = os.getenv('SENDER_EMAIL_PASSWORD')
    message = MIMEText(f'你的验证码为{code}，过期时间 60 秒', 'plain', 'utf-8')
    message['Subject'] = '你的验证码是'
    message['From'] = sender
    message['To'] = email
    try:
        smtp = smtplib.SMTP(host=os.getenv('SMTP_HOST'), port=int(os.getenv('SMTP_PORT')))
        smtp.starttls()
        smtp.login(sender, sender_pwd)
        smtp.sendmail(sender, email, message.as_string())
        smtp.quit()
    except Exception as e:
        print(e)
        return {
            'code':400,
            'msg':'发送失败',
            "data":None
        }

    # 验证码入库
    r = RedisUtil.get_redis_conn()

    r.set(email, code, ex=60)
    RedisUtil.close_redis_conn(r)
    return {
        'code':200,
        'msg':'发送成功',
        'data':{
            'username':username,
            'email':email,
        }
    }

def register_user(register_entity):
    result = UsersDao.check_email(register_entity.email)
    if result:   # 邮箱已存在
        return {
            'code': 400,
            'msg': '账号已注册',
            'data': None,
        }
    return UsersDao.add_user(
        register_entity.username,
        register_entity.email,
        register_entity.password,
    )

