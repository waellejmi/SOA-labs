from models import Product
from sqlalchemy.orm import Session


def create_product(db: Session, name: str, quantity: int, price: float) -> Product:
    product = Product(name=name, quantity=quantity, price=price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def update_product(
    db: Session, product_id: int, name: str, quantity: int, price: float
):
    product = get_product(db, product_id)
    if not product:
        return None
    product.name = name
    product.quantity = quantity
    product.price = price
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> bool:
    product = get_product(db, product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True


def get_all_products(db: Session):
    return db.query(Product).all()
