import functools
import os
import typing

import aiohttp.web
import jsonschema
import yaml

import billing

ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(billing.__file__), os.path.pardir),
)


def get_yaml():
    with open(os.path.join(ROOT_DIR, 'docs/api.yaml'), encoding='utf-8') as _f:
        return yaml.safe_load(_f)


def schema(ref: str) -> typing.Callable:

    def inner(handler):
        @functools.wraps(handler)
        async def wrapper(
                request: aiohttp.web.Request
        ) -> aiohttp.web.Response:
            if not hasattr(wrapper, 'yaml'):
                setattr(wrapper, 'yaml', get_yaml())

            validator = jsonschema.Draft4Validator(
                wrapper.yaml['definitions'][ref]
            )

            try:
                validator.validate(await request.json())
            except jsonschema.ValidationError as exc:
                return aiohttp.web.json_response(
                    {'error': str(exc)},
                    status=400,
                )
            return await handler(request)

        return wrapper
    return inner
