from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.admin import admin_bp
    from app.routes.stock import stock_bp
    from app.routes.analytics import analytics_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(analytics_bp)

    return app