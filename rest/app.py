from typing import List

from fastapi import Depends, FastAPI, HTTPException
from models import Base, SessionLocal, engine
from schemas import Product, ProductCreate, ProductUpdate
from service import (
    create_product,
    delete_product,
    get_all_products,
    get_product,
    update_product,
)
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory REST API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products", response_model=List[Product])
def read_products(db: Session = Depends(get_db)):
    return get_all_products(db)


@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", response_model=Product, status_code=201)
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product.name, product.quantity, product.price)


@app.put("/products/{product_id}", response_model=Product)
def update_product_route(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
):
    updated = update_product(
        db, product_id, product.name, product.quantity, product.price
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@app.delete("/products/{product_id}", status_code=204)
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    success = delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
