
import pytest
import mysql.connector

from app import app as flask_app
from config import Config

from repositories import (
    product_repository,
    cart_repository,
    order_repository
)

from services import order_service


def get_test_connection():
    """Connect exclusively to the isolated test database."""

    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database="grocery_test_db"
    )


@pytest.fixture
def client():
    flask_app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret-key"
    )

    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def test_database(monkeypatch):
    """
    Redirect repository connections to grocery_test_db.
    Clear test data before and after each integration test.
    """

    monkeypatch.setattr(
        product_repository,
        "get_connection",
        get_test_connection
    )

    monkeypatch.setattr(
        cart_repository,
        "get_connection",
        get_test_connection
    )

    monkeypatch.setattr(
        order_repository,
        "get_connection",
        get_test_connection
    )

    monkeypatch.setattr(
        order_service,
        "get_connection",
        get_test_connection
    )

    con = get_test_connection()
    cur = con.cursor()

    cur.execute("DELETE FROM orders")
    cur.execute("DELETE FROM cart")
    cur.execute("DELETE FROM stock")

    con.commit()
    cur.close()
    con.close()

    yield

    con = get_test_connection()
    cur = con.cursor()

    cur.execute("DELETE FROM orders")
    cur.execute("DELETE FROM cart")
    cur.execute("DELETE FROM stock")

    con.commit()
    cur.close()
    con.close()
