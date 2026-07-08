from flask import Blueprint, render_template
from app.services.stock_service import get_all_stock

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
def admin():
    stock = get_all_stock()
    return render_template("admin.html", stock=stock)