from typing import Optional
import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = True


class User(UserSchema):
    id: int
    email: str
    create_date: Optional[datetime.datetime] = datetime.datetime.now()


class UserForm(User):
    password: str


class UserSignUpForm(BaseModel):
    email: str
    password: str
