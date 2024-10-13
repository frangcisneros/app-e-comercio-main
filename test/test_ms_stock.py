import unittest
import requests
from threading import Thread
from app import create_app, db
import os


class StockTestCase(unittest.TestCase):
    def tearDown(self):
        response = requests.get("http://localhost:5000/api/v1/stock/get_all")
        json_data = response.json()
        for product in json_data:
            response = requests.delete(
                f"http://localhost:5000/api/v1/stock/delete_product/{product['product_id']}"
            )

    def test_stock_index(self):
        response = requests.get("http://127.0.0.1:5000/api/v1/stock")
        self.assertEqual(response.status_code, 200)

    def test_ms_stock_refuel(self):
        response = requests.post(
            "http://127.0.0.1:5000/api/v1/stock/refuel",
            json={"product_id": 1, "quantity": 10},
        )
        self.assertEqual(response.status_code, 200)

    def test_ms_stock_sell(self):
        response = requests.post(
            "http://localhost:5000/api/v1/stock/sell",
            json={"product_id": 1, "quantity": 5},
        )
        self.assertEqual(response.status_code, 200)

    def test_ms_stock_delete_product(self):
        response = requests.delete(
            "http://localhost:5000/api/v1/stock/delete_product/1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Product deleted successfully")

    def test_ms_check_quantity(self):
        response = requests.delete(
            "http://localhost:5000/api/v1/stock/delete_product/1"
        )
        response = requests.post(
            "http://127.0.0.1:5000/api/v1/stock/refuel",
            json={"product_id": 1, "quantity": 10},
        )

        response = requests.get("http://127.0.0.1:5000/api/v1/stock/check_quantity/1")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        self.assertEqual(response.json()["quantity"], 10)
