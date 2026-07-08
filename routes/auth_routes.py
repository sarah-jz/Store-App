from flask import Blueprint, render_template, request, redirect, url_for, session

from services.auth_service import verify_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def login():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login_user():

    username = request.form["username"]
    password = request.form["password"]

    user = verify_user(username, password)

    if not user:
        return "Invalid username or password"

    session["user_id"] = user[0]
    session["username"] = user[1]
    session["role"] = user[3]

    if user[3] == "admin":
        return redirect(url_for("admin.admin"))

    if user[3] == "staff":
        return redirect(url_for("admin.staff"))

    return redirect(url_for("shop.shop"))


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))