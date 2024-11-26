import unittest
import requests
from services.orquestador import saga_compra
from unittest.mock import patch


class TestSagaCompra(unittest.TestCase):
    def test_saga_compra_exito(self):

        requests.post(
            "http://127.0.0.1:5000/api/v1/stock/refuel",
            json={"product_id": 1, "quantity": 10},
        )

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
        requests.post(
            "http://127.0.0.1:5000/api/v1/stock/refuel",
            json={"product_id": 2, "quantity": 10},
        )
        data = {
            "pago_id": 1,
            "compra_id": 1,
            "producto_id": 9,
            "product_id": 9,
            "direccion_envio": "Calle Falsa 123",
            "precio": 100,
            "medio_pago": "tarjeta",
            # "quantity": 2,
        }
        response, status_code = saga_compra(data)
        print(response)


if __name__ == "__main__":
    unittest.main()
