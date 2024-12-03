import unittest
import requests


class ProductTestCase(unittest.TestCase):
    BASE_URL = "http://localhost:5003/api/v1"

    def tearDown(self):
        self.delete_all_products()

    def delete_all_products(self):
        response = requests.get(f"{self.BASE_URL}/get_all_products")
        json_data = response.json()
        for product in json_data:
            requests.delete(f"{self.BASE_URL}/delete_product/{product['id']}")

    def test_create_product(self):
        product_data = {"name": "Nuevo Producto4", "price": 150.0, "activated": True}
        response = requests.post(f"{self.BASE_URL}/create_product", json=product_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Producto Creado Correctamente")

    def test_get_product(self):
        requests.delete(f"{self.BASE_URL}/delete_product/0")
        product_data = {
            "id": 0,
            "name": "Producto de prueba",
            "price": 150.0,
            "activated": True,
        }
        requests.post(f"{self.BASE_URL}/create_product", json=product_data)
        response = requests.get(f"{self.BASE_URL}/get_product/0")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertIn("id", response_data[0])
        self.assertEqual(response_data[0]["id"], 0)
        self.assertEqual(response_data[0]["name"], "Producto de prueba")
        self.assertEqual(response_data[0]["price"], 150.0)
        self.assertTrue(response_data[0]["activated"])

    def test_delete_product(self):
        response = requests.delete(f"{self.BASE_URL}/delete_product/0")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Producto eliminado", response.text)


if __name__ == "__main__":
    unittest.main()
