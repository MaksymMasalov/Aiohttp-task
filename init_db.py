from sqlalchemy import create_engine, MetaData
import aiohttp
import asyncio

from app.settings import config
from app.db import users, units

dsn = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    """Creating tables"""

    meta = MetaData()
    meta.create_all(bind=engine, tables=[users, units])


async def sample_data():
    url = 'http://admin.geliospro.com/sdk/?login=demo&pass=demo&svc=get_users'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.text)
            return resp.text


if __name__ == '__main__':
    # db_url = dsn.format(**config['postgres'])
    # engine = create_engine(db_url)
    #
    # create_tables(engine)
    # sample_data(engine)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sample_data())
