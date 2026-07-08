from flask import Blueprint
from flask import jsonify
from services.analytics_service import *

from services.product_service import *

api_bp = Blueprint("api", __name__)
@api_bp.route("/api/products")
def api_products():

    products = get_all_products()

    result = []

    for p in products:

        result.append({

            "pcode": p[0],
            "name": p[1],
            "quantity": p[2],
            "price": p[3],
            "image": p[4],
            "description": p[5]

        })

    return jsonify(result)
@api_bp.route("/api/product/<int:pcode>")
def api_product(pcode):

    p = get_product(pcode)

    if not p:

        return jsonify({"error":"Product not found"}),404

    return jsonify({

        "pcode":p[0],
        "name":p[1],
        "quantity":p[2],
        "price":p[3],
        "image":p[4],
        "description":p[5]

    })
@api_bp.route("/api/dashboard")
def api_dashboard():

    return jsonify(

        get_dashboard_data()

    )