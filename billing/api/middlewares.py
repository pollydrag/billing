import logging

from aiohttp import web

logger = logging.getLogger(__name__)


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except Exception as exc:
        logger.exception(exc)
        return web.json_response(
            {'error': str(exc)},
            status=500,
        )
