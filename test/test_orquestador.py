import unittest
import requests
from services.orquestador import crear_orden
from unittest.mock import patch


class TestCrearOrden(unittest.TestCase):

    def test_crear_orden_exito(self):

        data = {"producto_id": 1, "cantidad": 2}

        response, status_code = crear_orden(data)

        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "Orden creada con éxito")

    @patch("requests.post")
    def test_crear_orden_fallo(self, mock_post):
        # Configurar el mock para que devuelva un fallo en el servicio de catálogo
        mock_post.side_effect = [
            requests.Response(),  # Respuesta para la acción del catálogo (fallo simulado)
            requests.Response(),  # Respuesta para la acción de compra (si llegara a ejecutarse)
            requests.Response(),  # Respuesta para la acción de pago (si llegara a ejecutarse)
        ]

        # Configuramos un fallo en la primera llamada
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = {"status": "Error"}

        data = {"producto_id": -1, "cantidad": -1}

        response, status_code = crear_orden(data)

        self.assertEqual(status_code, 500)
        self.assertEqual(response["status"], "Error al crear la orden")
        self.assertIn("Error", response["detail"])


if __name__ == "__main__":
    unittest.main()
