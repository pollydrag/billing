from aiohttp import web


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except Exception as exc:
        return web.json_response(
            {'error': str(exc)},
            status=500,
        )
