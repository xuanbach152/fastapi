from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate,ProductUpdate
from app.exception import NotFoundException,BadRequestException,ConflictException
import os
from fastapi import UploadFile
UPLOAD_DIR="app/image/product"

def get_all_product(db:Session):
    return db.query(Product).all()

def create_product(db:Session,product_data:ProductCreate):
    exist_product = db.query(Product).filter(Product.name == product_data.name).first()
    if exist_product:
        raise ConflictException("Product exist")
    category = db.query(Category).filter(Category.name == product_data.category_name).first()
    if not category:
        raise NotFoundException("Category not found")

    product = Product(name=product_data.name,description=product_data.description,price=product_data.price,
                      image=product_data.image,category_name=product_data.category_name)
    try:
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    except Exception:
        db.rollback()
        raise BadRequestException


def get_product(db:Session,product_id:int):
    product = db.query(Product).filter(Product.id==product_id).first()
    if not product:
        raise NotFoundException("Product Not Found")
    return product

def delete_product(db:Session,product_id:int):
    product = db.query(Product).filter(Product.id==product_id).first()
    if not product:
        raise NotFoundException("Product Not Found")
    try:
        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully", "id": product_id}

    except Exception:
        db.rollback()
        raise BadRequestException

def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise NotFoundException("Product Not Found")

    product_update = product_data.model_dump(exclude_unset=True)

    if "name" in product_update:
        existing = db.query(Product).filter(Product.name == product_update["name"], Product.id != product_id).first()
        if existing:
            raise ConflictException("Product name already exists")

    if "category_name" in product_update:
        category = db.query(Category).filter(Category.name == product_update["category_name"]).first()
        if not category:
            raise NotFoundException("Category not found")

    try:
        for key, value in product_update.items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product
    except Exception:
        db.rollback()
        raise BadRequestException
    
def upload_product_image(db: Session, product_id: int, file: UploadFile):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise NotFoundException("Product not found")

    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg",".jfif")):
        raise BadRequestException("Only PNG, JPG, JPEG, JFIF files are allowed")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"product_{product_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    product.image = filename
    try:
        db.commit()
        db.refresh(product)
        return product
    except Exception:
        db.rollback()
        raise BadRequestException("Không thể lưu ảnh vào DB")