import aiohttp.web
from aiopg import sa

from billing.api import routes
from billing.api import middlewares


def create_app():
    app = aiohttp.web.Application(
        middlewares=[middlewares.error_middleware]
    )
    app.on_startup.append(on_startup)
    routes.setup_routes(app)
    return app


async def on_startup(app: aiohttp.web.Application):
    app.db = await create_db()


async def create_db() -> sa.SAConnection:
    engine = await sa.create_engine(
        user='postgres',
        database='billing',
        host='127.0.0.1',
    )
    return await engine.acquire()


def main():
    aiohttp.web.run_app(create_app(), host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
