import unittest
import requests
from threading import Thread
from app import create_app, db
import os


class StockTestCase(unittest.TestCase):

    def setUp(self):
        os.environ["FLASK_ENV"] = "testing"
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_stock_index(self):
        response = requests.get("http://127.0.0.1:5000/api/v1/stock")
        self.assertEqual(response.status_code, 200)

    def test_ms_stock_refuel(self):
        response = requests.post(
            "http://127.0.0.1:5000/api/v1/stock/refuel",
            json={"product_id": 1, "quantity": 10},
        )
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_ms_check_quantity(self):
        # Primero reabastecer
        response = requests.post(
            "http://127.0.0.1:5000/api/v1/stock/refuel",
            json={"product_id": 1, "quantity": 10},
        )
        self.assertEqual(response.status_code, 200)

        # Ahora verificar la cantidad
        response = requests.get("http://127.0.0.1:5000/api/v1/stock/check_quantity/1")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        self.assertEqual(response.json()["quantity"], 10)