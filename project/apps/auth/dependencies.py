import datetime
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from config.db import users, database
from apps.users.models import User, UserForm
from config.settings import SECRET_KEY, ALGORITHM


token_auth_scheme = HTTPBearer()


class Token(BaseModel):
    scheme: str
    credentials: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """
    Function to verify user password.
    :param plain_password: plain user password
    :param hashed_password: hashed user password stored in database
    :return: ``True`` if the password matched the hash, else ``False``.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Get the hashed password from the plain one.
    :param password: plain password
    :return: hashed password
    """
    return pwd_context.hash(password)


async def get_user(email: str):
    """
    Get the user information using the user email.
    :param email: user email
    :return: user information
    """
    query = users.select().where(email == users.c.email)
    user = await database.fetch_one(query=query)
    if user:
        return UserForm(**user)


async def authenticate_user(email: str, password: str):
    """
    Authenticate user.
    :param email: user email
    :param password: user password
    :return: user if the authentication is valid otherwise ``False``
    """
    user = await get_user(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    """
    Create access token.
    :param data: user data
    :param expires_delta: expiration time
    :return: access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get current user using access token.
    :param token: access token
    :return: user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(email=email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Get current active user.
    :param current_user: user
    :return: user if user is active
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


