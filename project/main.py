from fastapi import FastAPI
from config.db import database, metadata, engine
from apps.dogs import router as dog_router
from apps.users import router as user_router
from apps.auth import router as auth_router
from apps.files import router as file_router

metadata.create_all(engine)

app = FastAPI()


@app.on_event('startup')
async def startup():
    """
    API startup.
    :return: None
    """
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    """
    API shutdown.
    :return:
    """
    await database.disconnect()

# Here are added all the routers for each app
app.include_router(dog_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(file_router.router)
