"""
JWT utilities and FastAPI dependencies.
"""

from datetime import datetime, timezone
from typing import Dict

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DELTA

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def create_access_token(claims: Dict) -> str:
    """
    Create a signed JWT access token with expiration.
    """
    to_encode = claims.copy()
    expire = datetime.now(tz=timezone.utc) + ACCESS_TOKEN_EXPIRE_DELTA
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_subject(token: str = Depends(oauth2_scheme)) -> str:
    """
    Validate Bearer token and return subject.
    """
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except PyJWTError:
        raise exc
    sub = payload.get("sub")
    if not sub:
        raise exc
    return sub
