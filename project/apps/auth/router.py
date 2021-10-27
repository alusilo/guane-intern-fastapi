from fastapi import APIRouter, HTTPException, status, Form
from apps.auth.dependencies import Token, authenticate_user, create_access_token
from config.settings import TOKEN_EXPIRE
import datetime

router = APIRouter()


@router.post("/api/token", response_model=Token)
async def login_for_access_token(email: str = Form(...), password: str = Form(...)):
    """
    Login to get access token.
    :param email: user email
    :param password: user password
    :return: dictionary containing scheme and access token
    """
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        access_token_expires = datetime.timedelta(minutes=TOKEN_EXPIRE)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"credentials": access_token, "scheme": "Bearer"}
