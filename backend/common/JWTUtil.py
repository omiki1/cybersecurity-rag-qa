from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
import secrets

from redis import RedisError

from common import RedisUtil

load_dotenv()

# 生成token,dict需要传user_id,username还有role_name
def create_access_token(data: dict):
    copy_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    copy_data.update({
        "exp": expire,  # 过期时间
        "iat": datetime.now(timezone.utc),  # 生成时间
        "user_id": data.get("user_id"),
        "username": data.get("username"),
        "role_name": data.get("role_name"),
        "jti": secrets.token_hex(8)

    })
    return jwt.encode(copy_data, key=os.getenv("SECRET_KEY"), algorithm="HS256")

def verify_token(token):
    try:
        payload = jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=["HS256"])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token已过期或错误",
        )
    jti = payload.get("jti")
    if jti:
        try:
            r = RedisUtil.get_redis_conn()
            blacklisted = r.exists(f"blacklist:{jti}")
            if blacklisted:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="token已失效，请重新登录"
                )
        except Exception as e:
            print(e)
            raise
    return payload


if __name__ == '__main__':
    token = create_access_token({"user_id": 1, "username": "ll", "role_name": "admin"})
    print(token)
    print(verify_token(token))