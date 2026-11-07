
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash
)

from services.order_service import checkout_user
from services.cart_service import cart_items, cart_total

from repositories.order_repository import (
    get_orders_by_user,
    get_total_spent
)


order_bp = Blueprint("order", __name__)


# ---------------- CHECKOUT PAGE ---------------- #

@order_bp.route("/checkout")
def checkout():

    if "username" not in session:
        return redirect(url_for("auth.login"))

    username = session["username"]

    items = cart_items(username)

    if not items:
        flash("Your cart is empty.")
        return redirect(url_for("order.order_history"))

    total = cart_total(items)

    return render_template(
        "checkout.html",
        items=items,
        cart_items=items,
        total=total,
        cart_total=total
    )


# ---------------- PROCESS CHECKOUT ---------------- #

@order_bp.route("/checkout", methods=["POST"])
@order_bp.route("/checkout/confirm", methods=["POST"])
def confirm_checkout():

    if "username" not in session:
        return redirect(url_for("auth.login"))

    username = session["username"]

    try:

        total = checkout_user(username)

        flash(
            f"Order placed successfully! Total: ₹{total}"
        )

        return redirect(url_for("order.order_history"))

    except ValueError as error:

        flash(str(error))

        return redirect(url_for("order.checkout"))

    except Exception:

        flash(
            "Something went wrong while processing your order."
        )

        return redirect(url_for("order.checkout"))


# ---------------- ORDER HISTORY ---------------- #

@order_bp.route("/orders")
def order_history():

    if "username" not in session:
        return redirect(url_for("auth.login"))

    username = session["username"]

    orders = get_orders_by_user(username)

    total_spent = get_total_spent(username)

    return render_template(
        "orders.html",
        orders=orders,
        total_spent=total_spent
    )
