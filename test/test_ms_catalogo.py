import unittest
import requests


class ProductTestCase(unittest.TestCase):
    def test_create_product(self):
        product_data = {"name": "Nuevo Producto4", "price": 150.0, "activated": True}
        response = requests.post(
            "http://localhost:5003/api/v1/create_product", json=product_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Producto Creado Correctamente")

    def test_get_product(self):
        response = requests.delete("http://localhost:5003/api/v1/delete_product/0")

        product_data = {
            "id": 0,
            "name": "Producto de prueba",
            "price": 150.0,
            "activated": True,
        }
        response = requests.post(
            "http://localhost:5003/api/v1/create_product", json=product_data
        )

        # Realizar la solicitud GET para obtener el producto por ID
        response = requests.get("http://localhost:5003/api/v1/get_product/0")
        self.assertEqual(response.status_code, 200)

        # Verificar el contenido de la respuesta JSON
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertIn("id", response_data[0])
        self.assertEqual(response_data[0]["id"], 0)
        self.assertEqual(response_data[0]["name"], "Producto de prueba")
        self.assertEqual(response_data[0]["price"], 150.0)
        self.assertTrue(response_data[0]["activated"])

    def test_delete_product(self):
        response = requests.delete("http://localhost:5003/api/v1/delete_product/0")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Producto eliminado", response.text)


if __name__ == "__main__":
    unittest.main()
