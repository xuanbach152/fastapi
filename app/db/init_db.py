# Table
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.option import Option
from app.models.product_option import ProductOption
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.cart_item_option import CartItemOption
from app.models.option_type import OptionType
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_item_option import OrderItemOption
from app.models.payment import Payment
from app.models.refresh_token import RefreshToken


from app.models.base import BaseModel

from app.db.database import SessionLocal, engine, Base

def init_database():
    BaseModel.metadata.create_all(bind=engine)