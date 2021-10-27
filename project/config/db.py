import databases
import sqlalchemy
from config.settings import DATABASE_URL

database = databases.Database(DATABASE_URL)
print(DATABASE_URL)
metadata = sqlalchemy.MetaData()

dogs = sqlalchemy.Table(
    'dogs',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('name', sqlalchemy.String, unique=True),
    sqlalchemy.Column('picture', sqlalchemy.String),
    sqlalchemy.Column('is_adopted', sqlalchemy.Boolean),
    sqlalchemy.Column('create_date', sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.sql.func.now())
)

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('email', sqlalchemy.String, unique=True),
    sqlalchemy.Column('password', sqlalchemy.String),
    sqlalchemy.Column('name', sqlalchemy.String),
    sqlalchemy.Column('last_name', sqlalchemy.String),
    sqlalchemy.Column('create_date', sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.sql.func.now()),
    sqlalchemy.Column('disabled', sqlalchemy.Boolean, server_default=sqlalchemy.sql.true()),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
