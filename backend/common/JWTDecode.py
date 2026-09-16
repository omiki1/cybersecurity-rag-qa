from fastapi.security import OAuth2PasswordBearer
from common.JWTUtil import verify_token
from typing import Annotated
import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import Depends, HTTPException, status


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not payload:
        raise credentials_exception
    else:
        return payload




