from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
import enum
from datetime import datetime

Base = declarative_base()


class OrderStatus(str, enum.Enum):
    in_progress = "в процессе"
    sent = "отправлен"
    delivered = "доставлен"


class Product(Base):
    """Модель для продукта"""
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)


class Order(Base):
    """Модель под заказ"""
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(OrderStatus))
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    """Модель для элемента заказа"""
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
