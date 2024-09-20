from pydantic import BaseModel
from typing import List, Optional
from models import OrderStatus


class ProductBase(BaseModel):
    """Базовая модель данных для продукта"""
    name: str
    description: str
    price: float
    quantity: int


class ProductCreate(ProductBase):
    """Для создания продукта"""
    id: int

    class Config:
        orm_mode = True


class ProductUpdate(BaseModel):
    """Для обновления продукта"""
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    quantity: Optional[int]


class OrderItemBase(BaseModel):
    """Базовая модель данных для элемента заказа"""
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderBase(BaseModel):
    """Базовая модель данных для заказа"""
    status: OrderStatus = OrderStatus.in_progress


class OrderCreate(OrderBase):
    id: int
    items: List[OrderItemCreate]

    class Config:
        orm_mode = True


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
