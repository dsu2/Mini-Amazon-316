from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .products import bp as products_bp
    app.register_blueprint(products_bp)

<<<<<<< HEAD
    from .purchases import bp as purchases_bp
    app.register_blueprint(purchases_bp)
=======
    from .cart import bp as cart_bp
    app.register_blueprint(cart_bp)

    from .Inventory import bp as inventory_bp
    app.register_blueprint(inventory_bp)
>>>>>>> 6f33248930a398a46ed1aa274c6fd96189cbce3e

    return app
