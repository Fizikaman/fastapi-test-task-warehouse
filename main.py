from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Base, Product, Order, OrderItem, OrderStatus
from schemas import ProductCreate, ProductUpdate, OrderCreate, OrderStatusUpdate
from database import engine, SessionLocal
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/products/", response_model=ProductCreate)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products/", response_model=List[ProductCreate])
def read_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


@app.get("/products/{product_id}", response_model=ProductCreate)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


@app.put("/products/{product_id}", response_model=ProductCreate)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).get(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    for var, value in vars(product).items():
        setattr(db_product, var, value) if value else None
    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).get(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    db.delete(db_product)
    db.commit()
    return {"detail": "Товар удален"}


@app.post("/orders/", response_model=OrderCreate)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Проверка наличия достаточного количества товаров
    for item in order.items:
        product = db.query(Product).get(item.product_id)
        if product is None or product.quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Недостаточно товара с ID {item.product_id}")
    db_order = Order(status=OrderStatus.in_progress)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    for item in order.items:
        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(db_order_item)
        product = db.query(Product).get(item.product_id)
        product.quantity -= item.quantity
        db.commit()
    return db_order


@app.get("/orders/", response_model=List[OrderCreate])
def read_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders


@app.get("/orders/{order_id}", response_model=OrderCreate)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


@app.patch("/orders/{order_id}/status", response_model=OrderCreate)
def update_order_status(order_id: int, status_update: OrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    order.status = status_update.status
    db.commit()
    db.refresh(order)
    return order
