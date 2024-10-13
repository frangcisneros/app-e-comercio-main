import unittest
import requests


class MainAppResourceTestCase(unittest.TestCase):
    def test_ms_pago(self):
        response = requests.get("http://localhost:5002/api/v1/pago")
        self.assertEqual(response.status_code, 200)

    def test_ms_pago_crear(self):
        response = requests.post(
            "http://localhost:5002/api/v1/pago",
            json={"producto_id": 1, "precio": 100.0, "medio_pago": "tarjeta"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_ms_obtener_todos_los_pagos(self):
        requests.post(
            "http://localhost:5002/api/v1/pago",
            json={"producto_id": 1, "precio": 100.0, "medio_pago": "tarjeta"},
        )
        requests.post(
            "http://localhost:5002/api/v1/pago",
            json={"producto_id": 2, "precio": 150.0, "medio_pago": "efectivo"},
        )
        response = requests.get("http://localhost:5002/api/v1/pago/todos")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()["pagos"]), 0)

    def test_crear_pago(self):
        response = requests.post(
            "http://localhost:5002/api/v1/pago",
            json={"producto_id": 1, "precio": 100.0, "medio_pago": "tarjeta"},
        )
        self.assertEqual(response.status_code, 201)

    def test_obtener_pago(self):
        response = requests.post(
            "http://localhost:5002/api/v1/pago",
            json={"producto_id": 1, "precio": 100.0, "medio_pago": "tarjeta"},
        )

        response = requests.get("http://localhost:5002/api/v1/pago/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["producto_id"], 1)
        self.assertEqual(response.json()["precio"], 100.0)
        self.assertEqual(response.json()["medio_pago"], "tarjeta")


if __name__ == "__main__":
    unittest.main()
