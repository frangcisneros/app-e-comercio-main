import logging
import requests
import os
from dotenv import load_dotenv
from pathlib import Path


basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, ".env"))


class CompraService:

    @staticmethod
    def crear_compra(data):
        r = requests.post(f"{os.getenv("MS_COMPRAS_URL")}/compras/", json=data)
        if r.status_code != 201:
            raise Exception("Error al crear la compra")
        else:
            data["compra_id"] = r.json()["id"]
            logging.info(r.json())

    @staticmethod
    def compensar_compra(compra_id):
        r = requests.delete(f"{os.getenv("MS_COMPRAS_URL")}/compras/{compra_id}")
        if r.status_code != 200:
            raise Exception("Error al compensar la compra")
        else:
            logging.error(r.json())
