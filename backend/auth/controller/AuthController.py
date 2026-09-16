from fastapi import APIRouter
from fastapi import Depends
from auth.service import AuthService
from common.JWTDecode import get_current_user
from user.entity.UserEntity import LoginByCodeEntity, LoginEntity

auth_router = APIRouter()

@auth_router.post("/login")
def password_login(login_entity: LoginEntity):
    return AuthService.password_login(login_entity)
@auth_router.post("/guestLogin")
def guest_login():
    """游客登录：无需密码，签发 role_name=guest 的 JWT，用于测试权限拦截"""
    return AuthService.guest_login()
@auth_router.post("/logout")
def logout(user: dict = Depends(get_current_user)):
    return AuthService.logout(user)
@auth_router.post("/loginByCode")
def login_by_code(login_entity: LoginByCodeEntity):
    return AuthService.login_by_code(login_entity)
