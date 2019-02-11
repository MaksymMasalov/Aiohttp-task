import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String
)

meta = MetaData()

users = Table(
    'users', meta,

    Column('id', Integer),
    Column('creator', Integer),
    Column('login', String(50))
)

units = Table(
    'units', meta,

    Column('id', Integer),
    Column('creator', Integer),
    Column('name', String(50))
)


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def get_users(conn):
    """Database query"""

    res = await conn.execute(users.select().order_by('id'))
    users_record = await res.fetchall()
    return users_record


async def get_units(conn):
    """Database query"""

    res = await conn.execute(units.select())
    units_record = await res.fetchall()

    return units_record


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
