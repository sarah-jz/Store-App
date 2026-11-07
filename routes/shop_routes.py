
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from services.product_service import (
    get_all_products,
    get_product
)

from services.cart_service import (
    add_to_cart,
    cart_items,
    cart_total,
    empty_cart
)

shop_bp = Blueprint("shop", __name__)


# ---------------- SHOP HOMEPAGE ---------------- #

@shop_bp.route("/shop")
def shop():

    if "username" not in session:
        return redirect(url_for("auth.login"))

    products = get_all_products()

    return render_template(
        "shop.html",
        products=products
    )


# ---------------- PRODUCT DETAILS ---------------- #

@shop_bp.route("/product/<int:pcode>")
def product_detail(pcode):

    if "username" not in session:
        return redirect(url_for("auth.login"))

    product = get_product(pcode)

    if not product:
        flash("Product not found.")
        return redirect(url_for("shop.shop"))

    return render_template(
        "product.html",
        product=product
    )


# ---------------- ADD TO CART ---------------- #

@shop_bp.route("/add_to_cart/<int:pcode>", methods=["POST"])
def add_product_to_cart(pcode):

    if "username" not in session:
        return redirect(url_for("auth.login"))

    try:
        quantity = int(request.form.get("quantity", 1))

        if quantity <= 0:
            raise ValueError

        product = get_product(pcode)

        if not product:
            flash("Product not found.")
            return redirect(url_for("shop.shop"))

        if quantity > product[2]:
            flash("Requested quantity exceeds available stock.")
            return redirect(url_for("shop.shop"))

        add_to_cart(
            session["username"],
            pcode,
            quantity
        )

        flash("Product added to cart.")

    except ValueError:
        flash("Please enter a valid quantity.")

    return redirect(url_for("shop.cart"))


# ---------------- VIEW CART ---------------- #

@shop_bp.route("/cart")
def cart():

    if "username" not in session:
        return redirect(url_for("auth.login"))

    items = cart_items(session["username"])

    total = cart_total(items)

    return render_template(
        "cart.html",
        cart=items,
        items=items,
        total=total
    )


# ---------------- REMOVE CART ITEM ---------------- #

@shop_bp.route("/remove_from_cart/<int:pcode>", methods=["POST"])
def remove_from_cart(pcode):

    if "username" not in session:
        return redirect(url_for("auth.login"))

    remove_item(
        session["username"],
        pcode
    )

    flash("Product removed from cart.")

    return redirect(url_for("shop.cart"))


# ---------------- UPDATE CART QUANTITY ---------------- #

@shop_bp.route("/update_cart/<int:pcode>", methods=["POST"])
def update_cart(pcode):

    if "username" not in session:
        return redirect(url_for("auth.login"))

    try:
        quantity = int(request.form.get("quantity", 0))

        if quantity <= 0:
            raise ValueError

        product = get_product(pcode)

        if not product:
            flash("Product not found.")
            return redirect(url_for("shop.cart"))

        if quantity > product[2]:
            flash("Requested quantity exceeds available stock.")
            return redirect(url_for("shop.cart"))

        update_quantity(
            session["username"],
            pcode,
            quantity
        )

        flash("Cart updated.")

    except ValueError:
        flash("Please enter a valid quantity.")

    return redirect(url_for("shop.cart"))
