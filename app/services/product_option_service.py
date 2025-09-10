from sqlalchemy.orm import Session
from app.models.product_option import ProductOption
from app.schemas.product_option import ProductOptionOut, ProductOptionBase
from app.exception import BadRequestException, ConflictException, ForbiddenException, NotFoundException, UnauthorizedException, InternalServerError


def create_product_option(db: Session, product_option: ProductOptionBase):
    product_id = product_option.product_id
    option_type_ids = product_option.option_type_ids
    product_option_new = []

    try:
        for otid in option_type_ids:
            exist = db.query(ProductOption).filter(
                ProductOption.product_id == product_id, ProductOption.option_type_id == otid).first()
            if exist:
                raise ConflictException
            new = ProductOption(product_id=product_id, option_type_id=otid)

            db.add(new)
            product_option_new.append(new)

        db.commit()
        for po in product_option_new:
            db.refresh(po)
        return product_option_new

    except Exception:
        db.rollback()
        raise BadRequestException
