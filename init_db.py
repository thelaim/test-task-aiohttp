from sqlalchemy import create_engine, MetaData

from app.settings import config
from app.db import block, page


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[block, page])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(page.insert(), [
        {'title': 'New Page',
         'slag': 'new-page'},
        {'title': 'Second Page',
         'slag': 'second-page'}
    ])
    conn.execute(block.insert(), [
        {'title': '5SOS', 'url': 'https://www.youtube.com/channel/UC-vKwDHcbPLtjml81ohGRng', 'block_id': 1, 'count_viewing': 0},
        {'title': 'Maroon 5', 'url': 'https://www.youtube.com/channel/UCBVjMGOIkavEAhyqpxJ73Dw', 'block_id': 2, 'count_viewing': 0},
        {'title': 'Imagine Dragons', 'url': 'https://www.youtube.com/channel/UCT9zcQNlyht7fRlcjmflRSA', 'block_id': 1, 'count_viewing': 0},
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)