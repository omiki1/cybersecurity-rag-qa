from fastapi import APIRouter
from user.service import UserService
from user.entity.UserEntity import RegisterEntity

users_router = APIRouter()

@users_router.get('/profile', summary='查询资料')
def get_profile(email: str):
    return UserService.get_profile(email)

@users_router.get('/sendEmail', summary='发送邮箱验证码')
def send_email(email: str):
    return UserService.send_email(email)


@users_router.post("/register")
def register_user(register_entity: RegisterEntity):
    return UserService.register_user(register_entity)
