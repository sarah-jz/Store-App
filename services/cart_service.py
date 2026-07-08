from repositories.cart_repository import *


def add_to_cart(username,pcode,qty):

    add_item(username,pcode,qty)


def cart_items(username):

    return get_cart(username)


def cart_total(items):

    total=0

    for item in items:

        total+=item[1]*item[2]

    return total


def empty_cart(username):

    clear_cart(username)