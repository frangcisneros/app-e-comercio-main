import unittest
import requests


class MainAppResourceTestCase(unittest.TestCase):
    BASE_URL = "http://localhost:5002/api/v1/pago"

    def tearDown(self):
        self.delete_all_pagos()

    def delete_all_pagos(self):
        response = requests.get(f"{self.BASE_URL}/todos")
        json_data = response.json()
        for product in json_data:
            requests.delete(f"{self.BASE_URL}/eliminar/{product['id']}")

    def test_ms_pago(self):
        response = requests.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_ms_pago_crear(self):
        response = requests.post(
            self.BASE_URL,
            json={"producto_id": 1, "precio": 100.0, "medio_pago": "tarjeta"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_crear_pago(self):
        response = requests.post(
            self.BASE_URL,
            json={"producto_id": 1, "precio": 100.0, "medio_pago": "tarjeta"},
        )
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
