from flask import Blueprint, render_template

stock_bp = Blueprint("stock", __name__)

@stock_bp.route("/stock")
def stock_page():
    return render_template("stock.html")