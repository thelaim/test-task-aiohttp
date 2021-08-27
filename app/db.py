import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String
)

__all__ = ['block', 'page']

meta = MetaData()

block = Table(
    'block', meta,

    Column('id', Integer, primary_key=True),
    Column('title', String(200), nullable=False),
    Column('url', String(200), nullable=False),
    Column('count_viewing', Integer),

    Column('block_id',
            Integer,
            ForeignKey('page.id', ondelete='CASCADE'))
)

page = Table(
    'page', meta,

    Column('id', Integer, primary_key=True),
    Column('title', String(200), nullable=False),
    Column('slag', String(200), nullable=False),

)

async def pg_context(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()


async def get_block(conn, block_id_url):
    result_sel = await conn.execute(
        block.select()
        .where(block.c.block_id == block_id_url)
        .order_by(block.c.id))

    result_up = await conn.execute(
        block.update()
            .returning(*block.c)
            .where(block.c.block_id == block_id_url)
            .values(count_viewing=block.c.count_viewing + 1))
    record = await result_up.fetchone()

    block_records = await result_sel.fetchall()
    return block_records