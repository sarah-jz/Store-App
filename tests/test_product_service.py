
from services import product_service


def test_get_all_products(monkeypatch):
    expected = [(101, "Rice", 20, 50, "rice.png", "Basmati rice")]

    monkeypatch.setattr(
        product_service, "repo_get_all_products",
        lambda: expected
    )

    assert product_service.get_all_products() == expected


def test_get_product(monkeypatch):
    expected = (101, "Rice", 20, 50, "rice.png", "Basmati rice")

    monkeypatch.setattr(
        product_service, "repo_get_product",
        lambda pcode: expected if pcode == 101 else None
    )

    assert product_service.get_product(101) == expected
    assert product_service.get_product(999) is None


def test_add_product(monkeypatch):
    calls = []

    monkeypatch.setattr(
        product_service, "insert_product",
        lambda *args: calls.append(args)
    )

    product_service.add_product(
        101, "Rice", 20, 50, "rice.png", "Basmati rice"
    )

    assert calls == [
        (101, "Rice", 20, 50, "rice.png", "Basmati rice")
    ]


def test_delete_product(monkeypatch):
    calls = []

    monkeypatch.setattr(
        product_service, "repo_delete_product",
        lambda pcode: calls.append(pcode)
    )

    product_service.delete_product(101)

    assert calls == [101]


def test_update_price(monkeypatch):
    calls = []

    monkeypatch.setattr(
        product_service, "update_product_price",
        lambda pcode, price: calls.append((pcode, price))
    )

    product_service.update_price(101, 60)

    assert calls == [(101, 60)]


def test_update_description(monkeypatch):
    calls = []

    monkeypatch.setattr(
        product_service, "update_product_description",
        lambda pcode, description: calls.append((pcode, description))
    )

    product_service.update_description(101, "Premium basmati rice")

    assert calls == [(101, "Premium basmati rice")]


def test_update_stock(monkeypatch):
    calls = []

    monkeypatch.setattr(
        product_service, "repo_update_stock",
        lambda pcode, quantity: calls.append((pcode, quantity))
    )

    product_service.update_stock(101, 30)

    assert calls == [(101, 30)]


def test_reduce_stock(monkeypatch):
    calls = []

    monkeypatch.setattr(
        product_service, "repo_reduce_stock",
        lambda pcode, quantity: calls.append((pcode, quantity))
    )

    product_service.reduce_stock(101, 5)

    assert calls == [(101, 5)]


def test_get_available_stock(monkeypatch):
    monkeypatch.setattr(
        product_service, "repo_get_available_stock",
        lambda pcode: 15 if pcode == 101 else 0
    )

    assert product_service.get_available_stock(101) == 15
    assert product_service.get_available_stock(999) == 0
