import unittest
from flask import current_app
from app import create_app
import os
import requests


class MainAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_request_items(self):
        # Crear un producto en el ms catalogo
        product_data = {
            "id": 0,
            "name": "Nuevo Producto4",
            "price": 150.0,
            "activated": True,
        }

        response = requests.post(
            "http://localhost:5003/api/v1/create_product", json=product_data
        )
        # Realizar la solicitud GET para obtener el producto por ID al ms catalogo
        response = self.app.test_client().get("/api/v1/get_product/0")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsNotNone(json_data)
        self.assertIsNotNone(json_data[0]["name"])
        # Eliminar el producto del ms catalogo
        response = requests.delete("http://localhost:5003/api/v1/delete_product/0")

    def test_buy_items(self):
        # Crear un producto en el ms catalogo
        product_data = {
            "id": 0,
            "name": "Nuevo Producto4",
            "price": 150.0,
            "activated": True,
        }

        response = requests.post(
            "http://localhost:5003/api/v1/create_product", json=product_data
        )
        # Crear un producto en el ms stock
        response = requests.post(
            "http://127.0.0.1:5000/api/v1/stock/refuel",
            json={"product_id": 0, "quantity": 1},
        )
        self.assertEqual(response.status_code, 200)
        # Realizar la solicitud POST para comprar el producto por ID al ms catalogo
        response = self.app.test_client().post("/api/v1/buy_product/0/1")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsNotNone(json_data)
        self.assertIsNotNone(json_data["message"])
        self.assertEqual(json_data["message"], "Sale made successfully")
        # Eliminar el producto del ms catalogo
        response = requests.delete("http://localhost:5003/api/v1/delete_product/0")


if __name__ == "__main__":
    unittest.main()
