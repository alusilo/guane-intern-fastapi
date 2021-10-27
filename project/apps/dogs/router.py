from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from config.db import database, dogs
from config.settings import STAGES, STAGING_TIME, CELERY_RESULT_BACKEND, RANDOM_IMAGES_SERVICE
from apps.dogs.models import Dog, DogSchema
from apps.auth.dependencies import Token, get_current_user, token_auth_scheme
import http3
import redis
from worker import move_to_next_stage

router = APIRouter()

client = http3.AsyncClient()

redis_info = redis.Redis.from_url(CELERY_RESULT_BACKEND)


@router.get('/api/dogs', response_model=List[Dog])
async def read_dogs():
    """
    Read all the dogs stored in database.
    :return: return a list of dogs
    """
    query = dogs.select()
    return await database.fetch_all(query=query)


@router.get('/api/dogs/{name}')
async def read_dog(name: str):
    """
    Read dog by name.
    :param name: name of the dog
    :return: dog
    """
    query = dogs.select().where(name == dogs.c.name)
    dog = await database.fetch_one(query=query)
    if not dog:
        raise HTTPException(status_code=404, detail='Dog not found')
    return dog


@router.get('/api/dogs/is_adopted/')
async def read_dog():
    """
    Read all adopted dogs.
    :return: list of adopted dogs
    """
    is_adopted = True
    query = dogs.select().where(is_adopted == dogs.c.is_adopted)
    return await database.fetch_all(query=query)


@router.get("/api/status/{name}")
async def status(name: str):
    """
    Get status of tasks.
    :param name: name of the task
    :return: task information
    """
    return redis_info.get(name)


@router.post('/api/dogs/{name}')
async def create_dog(name: str, payload: DogSchema, token: Token = Depends(token_auth_scheme)):
    """
    Create dog.
    :param name: dog name
    :param payload: dog information
    :param token: authentication token
    :return: dog information
    """
    user = await get_current_user(token.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    for i in range(len(STAGES)):
        move_to_next_stage.apply_async((name, STAGES[i]), countdown=i*STAGING_TIME)
    query = dogs.select().where(name == dogs.c.name)
    dog_exists = await database.execute(query=query)
    if dog_exists:
        raise HTTPException(status_code=403, detail='Dog already exists')
    else:
        img_response = await client.get(RANDOM_IMAGES_SERVICE)
        picture = img_response.json()['message']
        query = dogs.insert().values(
            user_id=user.id,
            name=name,
            picture=picture,
            is_adopted=payload.is_adopted
        ).returning(dogs.c.id)
        dog_id = await database.execute(query=query)

        query = dogs.select().where(dog_id == dogs.c.id)
        dog = await database.fetch_one(query=query)

        return dog


@router.put('/api/dogs/{name}')
async def update_dog(name: str, payload: DogSchema):
    """
    Update dog by name.
    :param name: dog name
    :param payload: Dog information
    :return: dog
    """
    query = dogs.select().where(name == dogs.c.name)
    dog = await database.fetch_one(query=query)
    if not dog:
        raise HTTPException(status_code=404, detail='Dog not found')

    query = dogs.update().where(name == dogs.c.name).values(
        is_adopted=payload.is_adopted
    ).returning(dogs.c.id)
    dog_id = await database.execute(query=query)

    query = dogs.select().where(dog_id == dogs.c.id)
    dog = await database.fetch_one(query=query)
    if not dog:
        raise HTTPException(status_code=404, detail='Dog not found')

    return dog


@router.delete('/api/dogs/{name}')
async def delete_dog(name: str):
    """
    Delete user.
    :param name: dog name
    :return: dictionary with dog name and a message of dog deletion
    """
    query = dogs.select().where(name == dogs.c.name)
    dog = await database.fetch_one(query=query)
    if not dog:
        raise HTTPException(status_code=404, detail='Dog does not exist')

    query = dogs.delete().where(name == dogs.c.name)
    dog_id = await database.execute(query=query)

    return {'name': name, 'detail': 'Dog deleted'}
