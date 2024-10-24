import logging
import requests


class CompraService:

    @staticmethod
    def crear_compra(data):
        r = requests.post("http://localhost:5001/compras/", json=data)
        if r.status_code != 201:
            raise Exception("Error al crear la compra")
        else:
            data["compra_id"] = r.json()["id"]
            logging.info(r.json())

    @staticmethod
    def compensar_compra(compra_id):
        r = requests.delete(f"http://localhost:5001/compras/{compra_id}")
        if r.status_code != 200:
            raise Exception("Error al compensar la compra")
        else:
            logging.error(r.json())
