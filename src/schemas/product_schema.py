from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    previous_price: float
    discount_percentage: float
    month: str
    initial_stock: int
    remaining_stock: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    previous_price: float | None = None
    discount_percentage: float | None = None
    month: str | None = None
    initial_stock: int | None = None
    remaining_stock: int | None = None


class Product(ProductBase):
    id: int
    enterprise_id: int

    class Config:
        from_attributes = True
