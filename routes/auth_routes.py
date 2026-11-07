
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash
)

from services.auth_service import verify_user, register_customer

auth_bp = Blueprint("auth", __name__)


# ---------------- LOGIN PAGE ---------------- #

@auth_bp.route("/")
def login():
    return render_template("login.html")


# ---------------- LOGIN ---------------- #

@auth_bp.route("/login", methods=["POST"])
def login_user():

    username = request.form["username"].strip()
    password = request.form["password"]

    user = verify_user(username, password)

    if not user:
        flash("Invalid username or password.")
        return redirect(url_for("auth.login"))

    session["user_id"] = user[0]
    session["username"] = user[1]
    session["role"] = user[3]

    if user[3] == "admin":
        return redirect(url_for("admin.admin"))

    if user[3] == "staff":
        return redirect(url_for("admin.staff"))

    return redirect(url_for("shop.shop"))


# ---------------- REGISTRATION PAGE ---------------- #

@auth_bp.route("/register")
def register():
    return render_template("register.html")


# ---------------- REGISTER CUSTOMER ---------------- #

@auth_bp.route("/register", methods=["POST"])
def register_user():

    username = request.form["username"].strip()
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
        flash("Passwords do not match.")
        return redirect(url_for("auth.register"))

    try:
        register_customer(username, password)

        flash("Account created successfully! You can now log in.")
        return redirect(url_for("auth.login"))

    except ValueError as error:
        flash(str(error))
        return redirect(url_for("auth.register"))

    except Exception:
        flash("Something went wrong while creating your account.")
        return redirect(url_for("auth.register"))


# ---------------- LOGOUT ---------------- #

@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))
