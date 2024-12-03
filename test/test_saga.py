import unittest
import requests
from services.saga import saga_compra
import os


class TestSagaCompra(unittest.TestCase):
    BASE_URL = "http://localhost:5000/api/v1/stock"

    def setUp(self):
        self.refuel_stock(1, 10)
        self.refuel_stock(2, 10)

    def refuel_stock(self, product_id, quantity):
        requests.post(
            f"{self.BASE_URL}/refuel",
            json={"product_id": product_id, "quantity": quantity},
        )

    def test_saga_compra_exito(self):
        data = {
            "producto_id": 1,
            "product_id": 1,
            "direccion_envio": "Calle Falsa 123",
            "precio": 100,
            "medio_pago": "tarjeta",
            "quantity": 2,
        }
        response, status_code = saga_compra(data)
        print(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "Orden creada con éxito")

    def test_saga_inventory_sell_error(self):
        data = {
            "producto_id": 1,
            "product_id": 1,
            "direccion_envio": "Calle Falsa 123",
            "precio": 100,
            "medio_pago": "tarjeta",
            # "quantity": 2,
        }
        response, status_code = saga_compra(data)
        print(response, status_code)
        self.assertEqual(status_code, 500)


if __name__ == "__main__":
    unittest.main()
