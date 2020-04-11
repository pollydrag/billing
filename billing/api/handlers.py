import aiohttp.web

from billing.api import models


async def ping(request: aiohttp.web.Request) -> aiohttp.web.Response:
    return aiohttp.web.Response(text='')


async def create_client(request: aiohttp.web.Request) -> aiohttp.web.Response:
    data = await request.json()
    db = request.app.db
    client_id = await models.create_client(db, data)
    client = await models.get_client(db, client_id)
    return aiohttp.web.json_response(client)


async def refill(request: aiohttp.web.Request) -> aiohttp.web.Response:
    data = await request.json()
    await models.refill_wallet(request.app.db, data)
    return aiohttp.web.json_response({})


async def transfer(request: aiohttp.web.Request) -> aiohttp.web.Response:
    data = await request.json()
    await models.transfer(request.app.db, data)
    return aiohttp.web.json_response({})
