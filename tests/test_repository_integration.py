
from decimal import Decimal

import pytest

from repositories import (
    product_repository,
    cart_repository,
    order_repository
)

from services.order_service import checkout_user


# ---------------------------------------
# PRODUCT REPOSITORY TESTS
# ---------------------------------------

def test_product_crud(test_database):

    product_repository.insert_product(
        101, "Rice", 50, 60, "rice.png", "Basmati rice"
    )

    product = product_repository.get_product(101)

    assert product is not None
    assert product[1] == "Rice"
    assert product[2] == 50
    assert product[3] == 60

    product_repository.update_product_price(101, 70)
    product_repository.update_product_description(
        101, "Premium basmati rice"
    )
    product_repository.update_stock(101, 40)

    product = product_repository.get_product(101)

    assert product[2] == 40
    assert product[3] == 70
    assert product[5] == "Premium basmati rice"

    product_repository.reduce_stock(101, 5)

    assert product_repository.get_available_stock(101) == 35

    product_repository.delete_product(101)

    assert product_repository.get_product(101) is None


def test_get_all_products(test_database):

    product_repository.insert_product(
        101, "Rice", 50, 60, "rice.png", "Rice"
    )

    product_repository.insert_product(
        102, "Milk", 30, 40, "milk.png", "Milk"
    )

    products = product_repository.get_all_products()

    assert len(products) == 2
    assert products[0][1] == "Milk"
    assert products[1][1] == "Rice"


# ---------------------------------------
# CART REPOSITORY TESTS
# ---------------------------------------

def test_cart_operations(test_database):

    product_repository.insert_product(
        101, "Rice", 50, 60, "rice.png", "Rice"
    )

    cart_repository.add_item("customer1", 101, 2)

    item = cart_repository.item_exists("customer1", 101)

    assert item is not None
    assert item[0] == 2

    cart = cart_repository.get_cart("customer1")

    assert len(cart) == 1
    assert cart[0][1] == "Rice"
    assert cart[0][2] == 2

    cart_repository.update_quantity("customer1", 101, 5)

    assert cart_repository.item_exists("customer1", 101)[0] == 5

    cart_repository.increase_quantity("customer1", 101, 3)

    assert cart_repository.item_exists("customer1", 101)[0] == 8

    cart_repository.remove_item("customer1", 101)

    assert cart_repository.item_exists("customer1", 101) is None


def test_clear_cart(test_database):

    product_repository.insert_product(
        101, "Rice", 50, 60, "rice.png", "Rice"
    )

    cart_repository.add_item("customer1", 101, 2)
    cart_repository.add_item("customer2", 101, 3)

    cart_repository.clear_cart("customer1")

    assert cart_repository.get_cart("customer1") == []
    assert len(cart_repository.get_cart("customer2")) == 1


# ---------------------------------------
# ORDER REPOSITORY TESTS
# ---------------------------------------

def test_order_operations(test_database):

    product_repository.insert_product(
        101, "Rice", 50, 60, "rice.png", "Rice"
    )

    order_repository.create_order(
        "customer1", 101, 2, 120
    )

    orders = order_repository.get_orders_by_user("customer1")

    assert len(orders) == 1
    assert orders[0][1] == "Rice"
    assert orders[0][2] == 2
    assert orders[0][3] == 120

    assert order_repository.get_total_spent("customer1") == 120
    assert order_repository.get_total_revenue() == 120
    assert order_repository.get_total_orders() == 1

    top_products = order_repository.get_top_products()

    assert len(top_products) == 1
    assert top_products[0][0] == "Rice"
    assert top_products[0][1] == 2


# ---------------------------------------
# REAL CHECKOUT INTEGRATION TESTS
# ---------------------------------------

def test_checkout_success(test_database):

    product_repository.insert_product(
        101, "Rice", 50, 60, "rice.png", "Rice"
    )

    cart_repository.add_item("customer1", 101, 2)

    total = checkout_user("customer1")

    assert total == Decimal("120")

    assert product_repository.get_available_stock(101) == 48

    assert cart_repository.get_cart("customer1") == []

    orders = order_repository.get_orders_by_user("customer1")

    assert len(orders) == 1
    assert orders[0][2] == 2
    assert orders[0][3] == 120


def test_checkout_insufficient_stock_rolls_back(test_database):

    product_repository.insert_product(
        101, "Rice", 2, 60, "rice.png", "Rice"
    )

    cart_repository.add_item("customer1", 101, 5)

    with pytest.raises(ValueError, match="Insufficient stock"):
        checkout_user("customer1")

    # Stock must remain unchanged.
    assert product_repository.get_available_stock(101) == 2

    # No order should have been created.
    assert order_repository.get_total_orders() == 0

    # Cart should remain available for the customer.
    cart = cart_repository.get_cart("customer1")

    assert len(cart) == 1
    assert cart[0][2] == 5
