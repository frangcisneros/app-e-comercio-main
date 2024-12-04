import unittest
import json
import requests


class TestComprasRoutes(unittest.TestCase):
    BASE_URL = "http://localhost:5001/compras"

    def tearDown(self):
        response = requests.get(self.BASE_URL)
        json_data = response.json()
        for compra in json_data:
            response = requests.delete(f"{self.BASE_URL}/{compra['id']}")

    def test_create_compra(self):
        data = {"producto_id": 1, "direccion_envio": "Calle Falsa 123"}
        response = requests.post(
            self.BASE_URL,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 201)
        json_data = response.json()
        self.assertEqual(json_data["producto_id"], 1)
        self.assertEqual(json_data["direccion_envio"], "Calle Falsa 123")

    def test_get_compra(self):
        data = {"producto_id": 1, "direccion_envio": "Calle Falsa 123"}
        response = requests.post(
            self.BASE_URL,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        compra = response.json()
        response = requests.get(f"{self.BASE_URL}/{compra['id']}")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data["producto_id"], 1)
        self.assertEqual(json_data["direccion_envio"], "Calle Falsa 123")

    def test_get_compras(self):
        data = {"producto_id": 1, "direccion_envio": "Calle Falsa 123"}
        requests.post(
            self.BASE_URL,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        data = {"producto_id": 2, "direccion_envio": "Calle 2"}
        requests.post(
            self.BASE_URL,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        response = requests.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data[0]["producto_id"], 1)
        self.assertEqual(json_data[1]["producto_id"], 2)

    def test_update_compra(self):
        data = {"producto_id": 1, "direccion_envio": "Calle Falsa 123"}
        response = requests.post(
            self.BASE_URL,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        compra = response.json()
        update_data = {"producto_id": 2, "direccion_envio": "Calle Actualizada 456"}
        response = requests.put(
            f"{self.BASE_URL}/{compra['id']}",
            data=json.dumps(update_data),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data["producto_id"], 2)
        self.assertEqual(json_data["direccion_envio"], "Calle Actualizada 456")

    def test_delete_compra(self):
        data = {"producto_id": 1, "direccion_envio": "Calle Falsa 123"}
        response = requests.post(
            self.BASE_URL,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        compra = response.json()
        response = requests.delete(f"{self.BASE_URL}/{compra['id']}")
        response = requests.get(f"{self.BASE_URL}/{compra['id']}")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
