from sqlalchemy.orm import Session
from app.models.option import Option
from app.schemas.option import OptionCreate
from app.exception import BadRequestException, ConflictException, ForbiddenException, NotFoundException, UnauthorizedException, InternalServerError


def create_option(db: Session, option: OptionCreate):
    exist_option = db.query(Option).filter(Option.name == option.name).first()
    if exist_option:
        raise ConflictException
    option = Option(name=option.name, extra_price=option.extra_price,
                    option_type_id=option.option_type_id)
    try:
        db.add(option)
        db.commit()
        db.refresh(option)
        return option
    except Exception:
        db.rollback()
        raise BadRequestException
