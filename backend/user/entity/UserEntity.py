from pydantic import BaseModel


class UserEntity(BaseModel):
    id: int | None = None
    email: str
    username: str
    password_hash: str | None = None
    role_name: str = 'user'

from pydantic import BaseModel, EmailStr, Field

class LoginEntity(BaseModel):
    email: EmailStr
    password: str

class LoginByCodeEntity(BaseModel):
    """验证码登录：邮箱 + 验证码"""
    email: EmailStr
    code: str = Field(min_length=4, max_length=4)
class RegisterEntity(BaseModel):
    email: EmailStr
    password: str
    username: str