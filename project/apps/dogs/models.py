from typing import Optional
import datetime
from pydantic import BaseModel


class DogSchema(BaseModel):
    is_adopted: bool


class Dog(DogSchema):
    id: int
    user_id: int
    name: str
    picture: Optional[str] = None
    create_date: Optional[datetime.datetime] = datetime.datetime.now()
