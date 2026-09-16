from fastapi import Header, HTTPException

from common.JWTDecode import get_current_user

def has_roles(*allowed_roles:list):
    """
       用法：Depends(has_roles(["admin"]))
       允许的角色列表传入后，检查当前用户 role_name 是否在其中。
       """

    def user_permission(authorization: str = Header(None)):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="缺少认证信息")
        token = authorization.split(" ")[1]
        current_user = get_current_user(token)
        if current_user['role_name'] in allowed_roles[0]:
            return current_user['username']
        else:
            raise HTTPException(status_code=403, detail="无访问权限")

    return user_permission