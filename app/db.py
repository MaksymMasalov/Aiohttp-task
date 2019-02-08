import aiopg.sa
from sqlalchemy.sql import select
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String
)

meta = MetaData()

users = Table(
    'users', meta,

    Column('id', Integer, primary_key=True),
    Column('creator', Integer),
    Column('login', String(50))
)

units = Table(
    'units', meta,

    Column('id', Integer, primary_key=True),
    Column('creator', Integer),
    Column('name', String(50))
)


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def get_users(conn):
    """Database query"""

    result = await conn.execute(select([users]))
    users_record = await result.fetchall()
    return users_record


async def startup(app):
    """Configuration info for a Postgres connection"""

    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def shutdown(app):
    """Close connection"""

    app['db'].close()
    await app['db'].wait_closed()
