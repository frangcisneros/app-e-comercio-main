import unittest
import requests
from threading import Thread
from app import create_app, db
import os


class StockTestCase(unittest.TestCase):
    BASE_URL = "http://localhost:5000/api/v1/stock"

    def tearDown(self):
        self.delete_all_products()

    def delete_all_products(self):
        response = requests.get(f"{self.BASE_URL}/get_all")
        json_data = response.json()
        for product in json_data:
            requests.delete(f"{self.BASE_URL}/delete_product/{product['product_id']}")

    def test_stock_index(self):
        response = requests.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_ms_stock_refuel(self):
        response = requests.post(
            f"{self.BASE_URL}/refuel", json={"product_id": 1, "quantity": 10}
        )
        self.assertEqual(response.status_code, 200)

    def test_ms_stock_sell(self):
        response = requests.post(
            f"{self.BASE_URL}/sell", json={"product_id": 1, "quantity": 5}
        )
        self.assertEqual(response.status_code, 200)

    def test_ms_stock_delete_product(self):
        response = requests.delete(f"{self.BASE_URL}/delete_product/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Product deleted successfully")

    def test_ms_check_quantity(self):
        self.delete_all_products()
        requests.post(f"{self.BASE_URL}/refuel", json={"product_id": 1, "quantity": 10})
        response = requests.get(f"{self.BASE_URL}/check_quantity/1")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        self.assertEqual(response.json()["quantity"], 10)
