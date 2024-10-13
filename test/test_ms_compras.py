import unittest
import json
import requests


class TestComprasRoutes(unittest.TestCase):
    def tearDown(self):
        # Obtener todas las compras a través de la API
        response = requests.get("http://localhost:5001/compras/")
        # eliminar todas las compras obtenidas
        json_data = response.json()
        for compra in json_data:
            response = requests.delete(f"http://localhost:5001/compras/{compra['id']}")

    def test_create_compra(self):
        # Datos para crear una nueva compra
        data = {"producto_id": 1, "direccion_envio": "Calle Falsa 123"}
        response = requests.post(
            "http://localhost:5001/compras/",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        # Verificar que la compra se haya creado correctamente
        self.assertEqual(response.status_code, 201)
        json_data = response.json()
        self.assertEqual(json_data["producto_id"], 1)
        self.assertEqual(json_data["direccion_envio"], "Calle Falsa 123")

    def test_get_compra(self):
        # Agregar una compra directamente a la base de datos
        data = {"producto_id": 1, "direccion_envio": "Calle Falsa 123"}
        response = requests.post(
            "http://localhost:5001/compras/",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        # Obtener la compra a través de la API
        compra = response.json()
        response = requests.get(f"http://localhost:5001/compras/{compra['id']}")
        self.assertEqual(response.status_code, 200)

        json_data = response.json()
        self.assertEqual(json_data["producto_id"], 1)
        self.assertEqual(json_data["direccion_envio"], "Calle Falsa 123")

    def test_get_compras(self):
        # Agregar varias compras
        data = {"producto_id": 1, "direccion_envio": "Calle Falsa 123"}
        response = requests.post(
            "http://localhost:5001/compras/",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        data = {"producto_id": 2, "direccion_envio": "Calle 2"}
        response = requests.post(
            "http://localhost:5001/compras/",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        # Obtener todas las compras a través de la API
        response = requests.get("http://localhost:5001/compras/")

        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data[0]["producto_id"], 1)
        self.assertEqual(json_data[1]["producto_id"], 2)

    def test_update_compra(self):
        data = {"producto_id": 1, "direccion_envio": "Calle Falsa 123"}
        response = requests.post(
            "http://localhost:5001/compras/",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        # Datos para actualizar la compra
        update_data = {"producto_id": 2, "direccion_envio": "Calle Actualizada 456"}

        # Actualizar la compra a través de la API
        compra = response.json()
        response = requests.put(
            f"http://localhost:5001/compras/{compra['id']}",
            data=json.dumps(update_data),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 200)

        # Verificar que la compra se haya actualizado correctamente
        json_data = response.json()
        self.assertEqual(json_data["producto_id"], 2)
        self.assertEqual(json_data["direccion_envio"], "Calle Actualizada 456")

    def test_delete_compra(self):
        data = {"producto_id": 1, "direccion_envio": "Calle Falsa 123"}
        response = requests.post(
            "http://localhost:5001/compras/",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        # Eliminar la compra a través de la API
        compra = response.json()
        response = requests.delete(f"http://localhost:5001/compras/{compra['id']}")

        # Verificar que la compra se haya eliminado correctamente
        response = requests.get(f"http://localhost:5001/compras/{compra['id']}")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
