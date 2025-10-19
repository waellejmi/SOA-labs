from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://wael:root@localhost:5432/inventory"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', quantity={self.quantity}, price={self.price})>"


def validate_product_data(quantity, price):
    if quantity < 0:
        raise ValueError("Quantity must be >= 0")
    if price < 0:
        raise ValueError("Price must be >= 0")


def create_product(name, quantity, price):
    validate_product_data(quantity, price)
    session = Session()
    try:
        new_product = Product(name=name, quantity=quantity, price=price)
        session.add(new_product)
        session.commit()
        print("Created:", new_product)
    except Exception as e:
        session.rollback()
        print("Error creating product:", e)
    finally:
        session.close()


def read_product(product_id):
    session = Session()
    try:
        product = session.query(Product).filter(Product.id == product_id).first()
        if product:
            print("Found:", product)
        else:
            print("Product not found.")
    finally:
        session.close()


def update_product(product_id, name=None, quantity=None, price=None):
    session = Session()
    try:
        product = session.query(Product).filter(Product.id == product_id).first()
        if not product:
            print("Product not found.")
            return
        if name is not None:
            product.name = name
        if quantity is not None:
            validate_product_data(quantity, product.price)
            product.quantity = quantity
        if price is not None:
            validate_product_data(product.quantity, price)
            product.price = price
        session.commit()
        print("Updated:", product)
    except Exception as e:
        session.rollback()
        print("Error updating product:", e)
    finally:
        session.close()


def delete_product(product_id):
    session = Session()
    try:
        product = session.query(Product).filter(Product.id == product_id).first()
        if product:
            session.delete(product)
            session.commit()
            print("Deleted product with ID:", product_id)
        else:
            print("Product not found.")
    except Exception as e:
        session.rollback()
        print("Error deleting product:", e)
    finally:
        session.close()


def list_all_products():
    session = Session()
    try:
        products = session.query(Product).all()
        if products:
            for p in products:
                print(p)
        else:
            print("No products found.")
    finally:
        session.close()


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    create_product("Laptop", 10, 999.99)
    create_product("Mouse", 50, 19.99)
    read_product(1)
    update_product(1, quantity=8)
    delete_product(2)
    list_all_products()
