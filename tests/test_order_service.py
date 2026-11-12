
from decimal import Decimal

import pytest
from services import order_service


class FakeConnection:
    def __init__(self):
        self.committed = False
        self.rolled_back = False
        self.closed = False
        self.transaction_started = False

    def start_transaction(self):
        self.transaction_started = True

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True


def setup_checkout(monkeypatch, cart, product, stock_update=1):
    con = FakeConnection()
    saved_orders = []
    cleared_carts = []

    monkeypatch.setattr(
        order_service, "get_connection", lambda: con
    )

    monkeypatch.setattr(
        order_service.cart_repository,
        "get_cart_with_connection",
        lambda connection, username: cart
    )

    monkeypatch.setattr(
        order_service.product_repository,
        "get_product_with_connection",
        lambda connection, pcode: product
    )

    monkeypatch.setattr(
        order_service.order_repository,
        "create_order_with_connection",
        lambda connection, username, pcode, quantity, total:
            saved_orders.append((username, pcode, quantity, total))
    )

    monkeypatch.setattr(
        order_service.product_repository,
        "reduce_stock_with_connection",
        lambda connection, pcode, quantity: stock_update
    )

    monkeypatch.setattr(
        order_service.cart_repository,
        "clear_cart_with_connection",
        lambda connection, username: cleared_carts.append(username)
    )

    return con, saved_orders, cleared_carts


def test_successful_checkout(monkeypatch):
    con, orders, cleared = setup_checkout(
        monkeypatch,
        cart=[(101, 2)],
        product=(101, "Rice", 10, Decimal("50.00"))
    )

    total = order_service.checkout_user("customer1")

    assert total == Decimal("100.00")
    assert orders == [
        ("customer1", 101, 2, Decimal("100.00"))
    ]
    assert cleared == ["customer1"]
    assert con.committed is True
    assert con.rolled_back is False
    assert con.closed is True


def test_checkout_empty_cart(monkeypatch):
    con, orders, cleared = setup_checkout(
        monkeypatch,
        cart=[],
        product=None
    )

    with pytest.raises(ValueError, match="cart is empty"):
        order_service.checkout_user("customer1")

    assert orders == []
    assert cleared == []
    assert con.rolled_back is True
    assert con.committed is False


def test_checkout_insufficient_stock(monkeypatch):
    con, orders, cleared = setup_checkout(
        monkeypatch,
        cart=[(101, 15)],
        product=(101, "Rice", 10, Decimal("50.00"))
    )

    with pytest.raises(ValueError, match="Insufficient stock"):
        order_service.checkout_user("customer1")

    assert orders == []
    assert cleared == []
    assert con.rolled_back is True
    assert con.committed is False


def test_checkout_product_not_found(monkeypatch):
    con, orders, cleared = setup_checkout(
        monkeypatch,
        cart=[(999, 2)],
        product=None
    )

    with pytest.raises(ValueError, match="no longer exists"):
        order_service.checkout_user("customer1")

    assert orders == []
    assert cleared == []
    assert con.rolled_back is True


def test_checkout_stock_update_failure(monkeypatch):
    con, orders, cleared = setup_checkout(
        monkeypatch,
        cart=[(101, 2)],
        product=(101, "Rice", 10, Decimal("50.00")),
        stock_update=0
    )

    with pytest.raises(ValueError, match="Could not update stock"):
        order_service.checkout_user("customer1")

    assert con.rolled_back is True
    assert con.committed is False
    assert cleared == []
