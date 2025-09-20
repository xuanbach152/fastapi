from sqlalchemy.orm import Session
from app.exception import BadRequestException, ConflictException, ForbiddenException, NotFoundException, UnauthorizedException, InternalServerError
from app.schemas.cart import CartItemCreate, CartItemResponse
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.cart_item_option import CartItemOption


def add_to_cart(db: Session, cartitem: CartItemCreate, user_id: int):
    try:
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)

        existing_item = db.query(CartItem).filter(
            CartItem.product_id == cartitem.product_id, CartItem.cart_id == cart.id).first()
        if existing_item:
            db_options = [opt.option_id for opt in db.query(CartItemOption)
                          .filter(CartItemOption.cart_item_id == existing_item.id)
                          .all()]
            if set(db_options) == set(cartitem.options):

                existing_item.quantity += cartitem.quantity
                db.commit()
                db.refresh(existing_item)
                return CartItemResponse(id=existing_item.id, quantity=existing_item.quantity, product_id=existing_item.product_id, options=db_options)

        newcartitem = CartItem(
            cart_id=cart.id, product_id=cartitem.product_id, quantity=cartitem.quantity)

        db.add(newcartitem)
        db.commit()
        db.refresh(newcartitem)

        if newcartitem:
            for cio in cartitem.options:
                itemoption = CartItemOption(
                    cart_item_id=newcartitem.id, option_id=cio)
                db.add(itemoption)

        db.commit()
        db.refresh(newcartitem)
        return CartItemResponse(id=newcartitem.id, quantity=newcartitem.quantity, product_id=newcartitem.product_id, options=cartitem.options)
    except Exception as e:
        db.rollback()
        raise BadRequestException(str(e))
