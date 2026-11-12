
from services import cart_service


def test_cart_total():
    items = [
        (101, "Rice", 2, 50, "rice.png"),
        (102, "Milk", 3, 30, "milk.png")
    ]

    assert cart_service.cart_total(items) == 190


def test_empty_cart_total():
    items = []

    assert cart_service.cart_total(items) == 0


def test_add_to_cart(monkeypatch):
    calls = []

    def fake_add_item(username, pcode, quantity):
        calls.append((username, pcode, quantity))

    monkeypatch.setattr(
        cart_service.cart_repository,
        "add_item",
        fake_add_item
    )

    cart_service.add_to_cart("customer1", 101, 2)

    assert calls == [("customer1", 101, 2)]


def test_remove_from_cart(monkeypatch):
    calls = []

    def fake_remove_item(username, pcode):
        calls.append((username, pcode))

    monkeypatch.setattr(
        cart_service.cart_repository,
        "remove_item",
        fake_remove_item
    )

    cart_service.remove_from_cart("customer1", 101)

    assert calls == [("customer1", 101)]


def test_update_cart_quantity(monkeypatch):
    calls = []

    def fake_update_quantity(username, pcode, quantity):
        calls.append((username, pcode, quantity))

    monkeypatch.setattr(
        cart_service.cart_repository,
        "update_quantity",
        fake_update_quantity
    )

    cart_service.update_cart_quantity("customer1", 101, 5)

    assert calls == [("customer1", 101, 5)]


def test_empty_cart(monkeypatch):
    calls = []

    def fake_clear_cart(username):
        calls.append(username)

    monkeypatch.setattr(
        cart_service.cart_repository,
        "clear_cart",
        fake_clear_cart
    )

    cart_service.empty_cart("customer1")

    assert calls == ["customer1"]
