from repositories.product_repository import (
    fetch_all_products,
    fetch_product,
    insert_product,
    delete_product as repo_delete_product,
    change_price,
    change_description
)

def get_all_products():

    return fetch_all_products()


def get_product(pcode):

    return fetch_product(pcode)


def add_product(pcode, name, qty, price, image, description):

    insert_product(
        pcode,
        name,
        qty,
        price,
        image,
        description
    )


def delete_product(pcode):

    repo_delete_product(pcode)


def update_price(pcode, price):

    change_price(pcode, price)


def update_description(pcode, description):

    change_description(pcode, description)