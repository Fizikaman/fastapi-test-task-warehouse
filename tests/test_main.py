from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_product():
    response = client.post("/products/", json={
        "name": "Товар 1",
        "description": "Описание товара 1",
        "price": 100.0,
        "quantity": 10
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Товар 1"


def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_create_order():
    response = client.post("/orders/", json={
        "items": [
            {"product_id": 1, "quantity": 2}
        ]
    })
    assert response.status_code == 200
    assert response.json()["status"] == "в процессе"
