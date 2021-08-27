from views import index, detail

def setup_routes(app):
    app.router.add_get('/', index),
    app.router.add_get('/{block_id}', detail, name='detail')