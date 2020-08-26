from aiohttp import web
import json
from models import session


def json_response(body='', **kwargs):
    kwargs['body'] = json.dumps(body or kwargs['body']).encode('utf-8')
    kwargs['content_type'] = 'text/json'
    return web.Response(**kwargs)


def get_models(Model):
    return session.query(Model)
