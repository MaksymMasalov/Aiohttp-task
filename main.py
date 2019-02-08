from aiohttp import web
import aiohttp_jinja2
import jinja2

from app.settings import config
from app.db import startup, shutdown
from app.routes import setup_routes


def main():

    app = web.Application()

    app['config'] = config

    aiohttp_jinja2.setup(
            app, loader=jinja2.PackageLoader('app', 'templates'))

    app.on_startup.append(startup)
    app.on_shutdown.append(shutdown)

    setup_routes(app)

    web.run_app(app)


if __name__ == '__main__':
    main()
