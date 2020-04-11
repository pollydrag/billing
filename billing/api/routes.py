import aiohttp.web

from billing.api import handlers


def setup_routes(app: aiohttp.web.Application):
    app.router.add_get('/ping', handlers.ping)
    app.router.add_post('/v1/clients', handlers.create_client)
    app.router.add_post('/v1/wallets/refill', handlers.refill)
    app.router.add_post('/v1/wallets/transfer', handlers.transfer)
