from sqlalchemy.orm import Session
from app.models.option_type import OptionType
from app.utils.const import OptionTypeEnum
from app.exception import BadRequestException, ConflictException, ForbiddenException, NotFoundException, UnauthorizedException, InternalServerError


def create_option_type(db: Session, optiontype: OptionTypeEnum):
    exist_type = db.query(OptionType).filter(
        OptionType.option_type == optiontype.value).first()
    if exist_type:
        raise ConflictException("Option type exist")
    new_option_type = OptionType(option_type=optiontype.value)
    try:
        db.add(new_option_type)
        db.commit()
        db.refresh(new_option_type)
        return new_option_type
    except Exception:
        db.rollback()
        raise BadRequestException


def get_all_option_type(db: Session):
    return db.query(OptionType).all()
