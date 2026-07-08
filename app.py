from flask import Flask
from flask_bcrypt import Bcrypt

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.shop_routes import shop_bp
from routes.order_routes import order_bp
from routes.api_routes import api_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(order_bp)
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(debug=True)