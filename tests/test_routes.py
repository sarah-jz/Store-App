
from routes import auth_routes, shop_routes, admin_routes


# ---------------- PUBLIC ROUTES ---------------- #

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_registration_page_loads(client):
    response = client.get("/register")
    assert response.status_code == 200


def test_shop_redirects_unauthenticated_user(client):
    response = client.get("/shop")

    assert response.status_code == 302
    assert response.location == "/"


def test_cart_redirects_unauthenticated_user(client):
    response = client.get("/cart")

    assert response.status_code == 302
    assert response.location == "/"


def test_product_redirects_unauthenticated_user(client):
    response = client.get("/product/101")

    assert response.status_code == 302
    assert response.location == "/"


def test_orders_redirect_unauthenticated_user(client):
    response = client.get("/orders")

    assert response.status_code == 302
    assert response.location == "/"


# ---------------- CUSTOMER LOGIN ---------------- #

def test_customer_login_success(client, monkeypatch):
    fake_user = (1, "customer1", "fake_password", "customer")

    monkeypatch.setattr(
        auth_routes,
        "verify_user",
        lambda username, password: fake_user
    )

    response = client.post(
        "/login",
        data={
            "username": "customer1",
            "password": "password123"
        }
    )

    assert response.status_code == 302
    assert response.location.endswith("/shop")

    with client.session_transaction() as session:
        assert session["user_id"] == 1
        assert session["username"] == "customer1"
        assert session["role"] == "customer"


# ---------------- ADMIN LOGIN ---------------- #

def test_admin_login_success(client, monkeypatch):
    fake_user = (2, "admin1", "fake_password", "admin")

    monkeypatch.setattr(
        auth_routes,
        "verify_user",
        lambda username, password: fake_user
    )

    response = client.post(
        "/login",
        data={
            "username": "admin1",
            "password": "password123"
        }
    )

    assert response.status_code == 302
    assert response.location.endswith("/admin")

    with client.session_transaction() as session:
        assert session["user_id"] == 2
        assert session["username"] == "admin1"
        assert session["role"] == "admin"


# ---------------- INVALID LOGIN ---------------- #

def test_invalid_login(client, monkeypatch):
    monkeypatch.setattr(
        auth_routes,
        "verify_user",
        lambda username, password: None
    )

    response = client.post(
        "/login",
        data={
            "username": "wronguser",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 302
    assert response.location == "/"

    with client.session_transaction() as session:
        assert "username" not in session
        assert "role" not in session


# ---------------- CUSTOMER ACCESS ---------------- #

def test_customer_can_access_shop(client, monkeypatch):
    monkeypatch.setattr(
        shop_routes,
        "get_all_products",
        lambda: []
    )

    with client.session_transaction() as session:
        session["user_id"] = 1
        session["username"] = "customer1"
        session["role"] = "customer"

    response = client.get("/shop")

    assert response.status_code == 200


def test_customer_cannot_access_admin(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["username"] = "customer1"
        session["role"] = "customer"

    response = client.get("/admin")

    assert response.status_code == 403
    assert response.get_data(as_text=True) == "Access Denied"


# ---------------- ADMIN ACCESS ---------------- #

def test_admin_can_access_admin(client, monkeypatch):
    monkeypatch.setattr(
        admin_routes,
        "get_all_products",
        lambda: []
    )

    with client.session_transaction() as session:
        session["user_id"] = 2
        session["username"] = "admin1"
        session["role"] = "admin"

    response = client.get("/admin")

    assert response.status_code == 200


def test_unauthenticated_user_cannot_access_admin(client):
    response = client.get("/admin")

    assert response.status_code == 302
    assert response.location == "/"


# ---------------- LOGOUT ---------------- #

def test_logout_clears_session(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["username"] = "customer1"
        session["role"] = "customer"

    response = client.get("/logout")

    assert response.status_code == 302
    assert response.location == "/"

    with client.session_transaction() as session:
        assert "user_id" not in session
        assert "username" not in session
        assert "role" not in session

    # The logged-out user should no longer access the shop.
    response = client.get("/shop")

    assert response.status_code == 302
    assert response.location == "/"
