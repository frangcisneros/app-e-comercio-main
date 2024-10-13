import unittest
import requests


class MainAppResourceTestCase(unittest.TestCase):
    def tearDown(self):
        response = requests.get("http://localhost:5002/api/v1/pago/todos")
        json_data = response.json()
        for product in json_data:
            response = requests.delete(
                f"http://localhost:5002/api/v1/pago/eliminar/{product['id']}"
            )

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

    def test_crear_pago(self):
        response = requests.post(
            "http://localhost:5002/api/v1/pago",
            json={"producto_id": 1, "precio": 100.0, "medio_pago": "tarjeta"},
        )
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
