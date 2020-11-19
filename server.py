import asyncio
import json
import logging
from base64 import urlsafe_b64decode
from datetime import datetime
from typing import Mapping

import uvloop
from aiohttp import web
from aiohttp.web_request import Request

logger = logging.getLogger(__name__)

routes = web.RouteTableDef()


def jwt_payload_decode(payload) -> dict:
    """Decodes the b64 url-encoded json payload of a jwt
       Note this is NOT the jwt itself, but rather just its payload.
       The expectation is that the JWT has already been validated and decoded.
    """
    # avoid padding errs by manually adding ===
    b64_decoded = urlsafe_b64decode(payload + '===')
    return json.loads(b64_decoded)


def text(request: Request):

    def dict_bullets(name: str, obj: Mapping) -> str:
        return name + '\n' + '\n'.join([f'* {k}: {v}' for k, v in obj.items()]) + '\n'

    resp_text = dict_bullets("HEADERS", request.headers)

    jwt_payload = request.headers.get("x-jwt-payload")
    if jwt_payload:
        decoded = jwt_payload_decode(jwt_payload)
        resp_text += dict_bullets("JWT", decoded)

    resp_text += f"Resp for {request.path} generated at {datetime.now()}\n"
    return resp_text


@routes.get("/error")
async def error(request: Request):
    logger.error("Responding with error")
    return web.Response(
        headers={
            "content-type": "text/plain; charset=UTF-8",
        },
        status=500,
        text=text(request),
    )


@routes.get("/timeout")
async def timeout(request: Request):
    logger.info("Sleeping...")
    await asyncio.sleep(10)
    return web.Response(
        headers={
            "content-type": "text/plain; charset=UTF-8",
        },
        status=500,
        text=text(request),
    )


@routes.get("/cache")
async def cache(request: Request):
    return web.Response(
        headers={
            "cache-control": "max-age=60",
            "content-type": "text/plain; charset=UTF-8",
        },
        text=text(request),
    )


@routes.get("/vary")
async def vary(request: Request):
    return web.Response(
        headers={
            "cache-control": "max-age=60",
            "content-type": "text/plain; charset=UTF-8",
            "vary": "x-api-key",
        },
        text=text(request),
    )


@routes.get("/rbac-read")
async def rbac_yes(request: Request):
    return web.Response(
        headers={
            "content-type": "text/plain; charset=UTF-8",
        },
        text=text(request),
    )


@routes.get("/rbac-write")
async def rbac_no(request: Request):
    return web.Response(
        headers={
            "content-type": "text/plain; charset=UTF-8",
        },
        text=text(request),
    )


@routes.get("/secure")
async def secure(request: Request):
    return web.Response(
        headers={
            "content-type": "text/plain; charset=UTF-8",
        },
        text=text(request),
    )


@routes.get("/{other}")
async def other(request: Request):
    return web.Response(
        headers={
            "content-type": "text/plain; charset=UTF-8",
        },
        text=text(request),
    )

if __name__ == '__main__':

    logging.basicConfig(level="INFO")

    app = web.Application()
    app.add_routes(routes)

    uvloop.install()
    web.run_app(app)
