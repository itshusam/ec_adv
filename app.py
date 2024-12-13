from flask import Flask
from database import db
from schema import ma
from limiter import limiter
from routes.customer_account_route import customer_account_bp
from routes.customer_route import customer_bp
from routes.product_route import product_bp
from routes.order_route import order_bp
from caching import cache
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from routes.user_route import auth_blueprint
SWAGGER_URL = '/api/docs'
API_URL = 'static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': " e-commerce"
    }
)
def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.unit_app(app)
    CORS(app)
    return app

def blue_print_config(app):
    app.register_blueprint(auth_blueprint, url_prefix='/login')
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(customer_account_bp, url_prefix='/employees')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(swaggerui_blueprint, url_prefix='/SWAGGER_URL')

def configure_rate_limit():
    limiter.limit("5 per day")(customer_bp)



if __name__ == '__main__':
    app = create_app('DevelopmentConfig')

    blue_print_config(app)
    configure_rate_limit()

    with app.app_context():
        db.drop_all()
        db.create_all()

    app.run(debug=True)