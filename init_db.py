from sqlalchemy import create_engine, MetaData
import aiohttp
import asyncio
import json

from app.settings import config
from app.db import users, units

dsn = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    """Creating tables"""

    meta = MetaData()
    meta.create_all(bind=engine, tables=[users, units])


async def sample_data():
    """Takes data from the link, decodes them and writes to the database"""

    url_users = 'http://admin.geliospro.com/sdk/?login=demo&pass=demo&svc=get_users'
    url_units = 'http://admin.geliospro.com/sdk/?login=demo&pass=demo&svc=get_units'
    conn = engine.connect()

    async with aiohttp.ClientSession() as session:
        async with session.get(url_users) as resp:
            print(resp.status)
            data = await resp.text()

        received_data = json.loads(data)
        for i in received_data:
            insert = users.insert().values(id=i['id'], creator=i['creator'], login=i['login'])
            conn.execute(insert)

        async with session.get(url_units) as r:
            print(r.status)
            data = await r.text()

        received_data = json.loads(data)
        for i in received_data:
            insert = units.insert().values(id=i['id'], creator=i['creator'], name=i['name'])
            conn.execute(insert)


if __name__ == '__main__':
    db_url = dsn.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(sample_data())
