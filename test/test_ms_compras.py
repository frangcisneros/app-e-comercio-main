import unittest
from app import create_app, db
import requests
import json


class ComprasTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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
        # Datos para crear una nueva compra
        data = {"producto_id": 1, "direccion_envio": "Calle Falsa 123"}
        response = requests.post(
            "http://localhost:5001/compras/",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        # Obtener la compra a través de la API
        response = requests.get("http://localhost:5001/compras/1")
        self.assertEqual(response.status_code, 200)

        json_data = response.json()
        self.assertEqual(json_data["producto_id"], 1)
        self.assertEqual(json_data["direccion_envio"], "Calle Falsa 123")

    def test_get_compras(self):
        # Datos para crear una nueva compra
        data = {"producto_id": 1, "direccion_envio": "Calle Falsa 123"}
        response = requests.post(
            "http://localhost:5001/compras/",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        # Datos para crear una nueva compra
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
        print(json_data)
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data[0]["producto_id"], 1)
        self.assertEqual(json_data[1]["producto_id"], 2)

    def test_update_compra(self):
        # Datos para crear una nueva compra
        data = {"producto_id": 1, "direccion_envio": "Calle Falsa 123"}
        response = requests.post(
            "http://localhost:5001/compras/",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        # Datos para actualizar la compra
        update_data = {"producto_id": 2, "direccion_envio": "Calle Actualizada 456"}

        # Actualizar la compra a través de la API
        response = self.client.put(
            f"/compras/{compra.id}",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # Verificar que la compra se haya actualizado correctamente
        json_data = json.loads(response.data)
        self.assertEqual(json_data["producto_id"], 2)
        self.assertEqual(json_data["direccion_envio"], "Calle Actualizada 456")

    def test_delete_compra(self):
        # Agregar una compra directamente a la base de datos
        compra = Compras.crear_compra(producto_id=1, direccion_envio="Calle Falsa 123")

        # Eliminar la compra a través de la API
        response = self.client.delete(f"/compras/{compra.id}")
        self.assertEqual(response.status_code, 200)

        # Verificar que la compra haya sido eliminada
        self.assertEqual(Compras.query.count(), 0)
