from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session

from services.product_service import *
from services.cart_service import *

shop_bp=Blueprint("shop",__name__)