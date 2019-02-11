from aiohttp import web
import aiohttp_jinja2

from app import db


async def index(request):
    return web.Response(text='Hello Aiohttp!')


@aiohttp_jinja2.template('get_users.html')
async def user(request):
    async with request.app['db'].acquire() as conn:
        users = await db.get_users(conn)
    return {'users': users}


@aiohttp_jinja2.template('get_units.html')
async def unit(request):
    async with request.app['db'].acquire() as conn:
        units = await db.get_units(conn)
    return {'units': units}
