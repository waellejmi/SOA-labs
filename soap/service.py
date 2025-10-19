from models import Product, SessionLocal
from spyne import Boolean, Float, Integer, ServiceBase, Unicode, rpc


class ProductService(ServiceBase):
    @rpc(Unicode(nullable=False), Integer, Float, _returns=Integer)
    def CreateProduct(ctx, name, quantity, price):
        if quantity < 0 or price < 0:
            raise ValueError("Quantity and price must be >= 0")
        session = SessionLocal()
        try:
            product = Product(name=name, quantity=quantity, price=price)
            session.add(product)
            session.commit()
            return product.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @rpc(Integer, _returns=Unicode)
    def GetProduct(ctx, product_id):
        session = SessionLocal()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if not product:
                return "Product not found"
            return f"ID: {product.id}, Name: {product.name}, Qty: {product.quantity}, Price: {product.price}"
        finally:
            session.close()

    @rpc(Integer, Unicode, Integer, Float, _returns=Boolean)
    def UpdateProduct(ctx, product_id, name, quantity, price):
        if quantity < 0 or price < 0:
            raise ValueError("Quantity and price must be >= 0")
        session = SessionLocal()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if not product:
                return False
            product.name = name
            product.quantity = quantity
            product.price = price
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()

    @rpc(Integer, _returns=Boolean)
    def DeleteProduct(ctx, product_id):
        session = SessionLocal()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if not product:
                return False
            session.delete(product)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
