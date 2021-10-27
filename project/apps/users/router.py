from typing import List
from fastapi import APIRouter, HTTPException
from config.db import database, users
from apps.users.models import UserForm, User, UserSchema, UserSignUpForm
from apps.auth.dependencies import get_password_hash

router = APIRouter()


@router.get('/api/users', response_model=List[User])
async def read_user():
    query = users.select()
    return await database.fetch_all(query=query)


@router.get('/api/users/{user_id}', response_model=User)
async def read_dog(user_id: int):
    query = users.select().where(user_id == users.c.id)
    user = await database.fetch_one(query=query)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.post('/api/signup')
async def create_user(user: UserSignUpForm):
    query = users.select().where(user.email == users.c.email)
    user_exists = await database.execute(query=query)
    if user_exists:
        raise HTTPException(status_code=403, detail='User already exists')
    else:
        query = users.insert().values(
            email=user.email,
            password=get_password_hash(user.password)
        ).returning(users.c.id)
        user_id = await database.execute(query=query)

        return {'id': user_id, 'email': user.email}


@router.put('/api/users/{user_id}', response_model=User)
async def update_dog(user_id: int, payload: UserSchema):
    query = users.select().where(user_id == users.c.id)
    user = await database.fetch_one(query=query)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    query = users.update().where(user_id == users.c.id).values(
        name=payload.name,
        last_name=payload.last_name,
        disabled=payload.disabled
    ).returning(users.c.id)
    user_id = await database.execute(query=query)

    query = users.select().where(user_id == users.c.id)
    user = await database.fetch_one(query=query)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    return user


@router.delete('/api/users/{user_id}')
async def delete_dog(user_id: int):
    query = users.select().where(user_id == users.c.id)
    user = await database.fetch_one(query=query)
    if not user:
        raise HTTPException(status_code=404, detail='User does not exist')

    query = users.delete().where(user_id == users.c.id)
    user = await database.execute(query=query)

    return {'id': user_id, 'detail': 'User deleted'}
