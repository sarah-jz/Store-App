from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from werkzeug.utils import secure_filename

import os

from services.user_service import role_required
from services.product_service import *

from config import Config

admin_bp = Blueprint("admin",__name__)


@admin_bp.route("/admin")
@role_required("admin")
def admin():

    stock=get_all_products()

    total_products=len(stock)

    return render_template(

        "admin.html",

        stock=stock,

        total_products=total_products

    )


@admin_bp.route("/add")
@role_required("admin")
def add():

    return render_template("add.html")


@admin_bp.route("/add_product",methods=["POST"])
@role_required("admin")
def add_product_route():

    pcode=request.form["pcode"]
    name=request.form["name"]
    qty=request.form["quantity"]
    price=request.form["price"]
    description=request.form["description"]

    image=request.files["image"]

    if image.filename=="":

        filename="default.png"

    else:

        filename=secure_filename(image.filename)

        image.save(

            os.path.join(

                Config.UPLOAD_FOLDER,

                filename

            )

        )

    add_product(

        pcode,

        name,

        qty,

        price,

        filename,

        description

    )

    return redirect(url_for("admin.admin"))


@admin_bp.route("/delete/<int:pcode>")
@role_required("admin")
def delete(pcode):

    delete_product(pcode)

    return redirect(url_for("admin.admin"))


@admin_bp.route("/update_price/<int:pcode>",methods=["POST"])
@role_required("admin")
def update_price_route(pcode):

    update_price(

        pcode,

        request.form["price"]

    )

    return redirect(url_for("admin.admin"))


@admin_bp.route("/update_description/<int:pcode>",methods=["POST"])
@role_required("admin")
def update_description_route(pcode):

    update_description(

        pcode,

        request.form["description"]

    )

    return redirect(

        url_for(

            "shop.product_detail",

            pcode=pcode

        )

    )