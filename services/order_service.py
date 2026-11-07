from database.db import get_connection

from repositories import cart_repository
from repositories import product_repository
from repositories import order_repository

from decimal import Decimal


def checkout_user(username):

    con = get_connection()

    try:

        # Start one database transaction
        con.start_transaction()

        # 1. Retrieve the customer's cart
        cart_items = cart_repository.get_cart_with_connection(
            con,
            username
        )

        if not cart_items:
            raise ValueError("Your cart is empty.")

        total_amount = Decimal("0.00")

        # 2. Validate products and stock
        for pcode, quantity in cart_items:

            quantity = int(quantity)

            if quantity <= 0:
                raise ValueError("Invalid product quantity.")

            product = product_repository.get_product_with_connection(
                con,
                pcode
            )

            if not product:
                raise ValueError(
                    f"Product {pcode} no longer exists."
                )

            product_code, product_name, available_stock, price = product

            if available_stock < quantity:
                raise ValueError(
                    f"Insufficient stock for {product_name}."
                )

            # Calculate the price using Decimal
            price = Decimal(str(price))

            item_total = price * quantity

            total_amount += item_total

            # 3. Insert order record
            order_repository.create_order_with_connection(
                con,
                username,
                product_code,
                quantity,
                item_total
            )

            # 4. Reduce stock
            updated_rows = product_repository.reduce_stock_with_connection(
                con,
                product_code,
                quantity
            )

            if updated_rows != 1:
                raise ValueError(
                    f"Could not update stock for {product_name}."
                )

        # 5. Clear the customer's cart
        cart_repository.clear_cart_with_connection(
            con,
            username
        )

        # 6. Commit everything together
        con.commit()

        return total_amount

    except Exception:

        # Undo all changes if anything fails
        con.rollback()

        raise

    finally:

        con.close()