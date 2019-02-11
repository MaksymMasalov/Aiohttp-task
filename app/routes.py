from app.views import index, user, unit


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/get_users', user)
    app.router.add_get('/get_units', unit)
