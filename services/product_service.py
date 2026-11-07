from repositories.product_repository import (
    get_all_products as repo_get_all_products,
    get_product as repo_get_product,
    insert_product,
    delete_product as repo_delete_product,
    update_product_price,
    update_product_description,
    update_stock as repo_update_stock,
    reduce_stock as repo_reduce_stock,
    get_available_stock as repo_get_available_stock
)


# ---------------- GET ALL PRODUCTS ---------------- #

def get_all_products():
    return repo_get_all_products()


# ---------------- GET SINGLE PRODUCT ---------------- #

def get_product(pcode):
    return repo_get_product(pcode)


# ---------------- ADD PRODUCT ---------------- #

def add_product(pcode, name, qty, price, image, description):
    insert_product(pcode, name, qty, price, image, description)


# ---------------- DELETE PRODUCT ---------------- #

def delete_product(pcode):
    repo_delete_product(pcode)


# ---------------- UPDATE PRICE ---------------- #

def update_price(pcode, price):
    update_product_price(pcode, price)


# ---------------- UPDATE DESCRIPTION ---------------- #

def update_description(pcode, description):
    update_product_description(pcode, description)


# ---------------- UPDATE STOCK ---------------- #

def update_stock(pcode, quantity):
    repo_update_stock(pcode, quantity)


# ---------------- REDUCE STOCK ---------------- #

def reduce_stock(pcode, quantity):
    repo_reduce_stock(pcode, quantity)


# ---------------- GET AVAILABLE STOCK ---------------- #

def get_available_stock(pcode):
    return repo_get_available_stock(pcode)