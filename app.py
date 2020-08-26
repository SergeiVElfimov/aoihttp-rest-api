from aiohttp import web
from router import *


def main(auth_middleware, routes):
    app = web.Application(
        middlewares=[auth_middleware]
    )

    for route in routes:
        app.router.add_route(
            route.method,
            route.url,
            route.handler,
            expect_handler=web.Request.json
        )
    return app


if __name__ == '__main__':
    app = main(auth_middleware, urlpatterns)
    web.run_app(app)
