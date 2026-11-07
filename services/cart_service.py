from repositories import cart_repository,
remove_from_cart, 
update_cart_quantity

# ---------------- ADD TO CART ---------------- #

def add_to_cart(username, pcode, qty):
    cart_repository.add_item(username, pcode, qty)


# ---------------- GET CART ITEMS ---------------- #

def cart_items(username):
    return cart_repository.get_cart(username)


# ---------------- CALCULATE CART TOTAL ---------------- #

def cart_total(items):
    total = 0

    for item in items:
        quantity = item[2]
        price = item[3]

        total += quantity * price

    return total


# ---------------- EMPTY CART ---------------- #

def empty_cart(username):
    cart_repository.clear_cart(username)

# ---------------- REMOVE CART ITEM ---------------- #

def remove_from_cart(username, pcode):
    cart_repository.remove_item(username, pcode)


# ---------------- UPDATE CART QUANTITY ---------------- #

def update_cart_quantity(username, pcode, quantity):
    cart_repository.update_quantity(username, pcode, quantity)