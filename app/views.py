from aiohttp import web
from sqlalchemy import select
import aiohttp
import aiohttp_jinja2

from app import db


async def index(request):
    return web.Response(text='Hello Aiohttp!')


@aiohttp_jinja2.template('get_users.html')
async def post(request):
    async with request.app['db'].acquire() as conn:
        query = select([db.users])
        print(query)
        result = await conn.execute(query)

    return aiohttp.web.Response(body=str(result))
