from typing import Any

from pydantic import BaseModel, field_validator


class ProductBase(BaseModel):
    name: str
    quantity: int
    price: float

    @field_validator("quantity", "price")
    @classmethod
    def non_negative(cls, v: Any, info) -> Any:
        if v < 0:
            raise ValueError(f"{info.field_name} must be >= 0")
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
