from aiohttp import web
from sqlalchemy import select

import db

import json

async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.block.select())
        records = await cursor.fetchall()
        pages = [dict(q) for q in records]
        title_url = []
        for i in pages:
            title_url.append(i['title'])
            id_page = i['block_id']
            title_url.append(f'http://127.0.0.1:8080/{id_page}')
        response_obj = {'data': title_url}
        return web.Response(text=json.dumps(response_obj))


async def detail(request):
    async with request.app['db'].acquire() as conn:
        block_id_url = int(request.match_info['block_id'])

        blocks = await db.get_block(conn, block_id_url)
        block = [dict(q) for q in blocks]
        obj = {
            'blocks': block,
        }
    return web.Response(text=json.dumps(obj))