import logging
import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_random

basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, ".env"))

if os.getenv("FLASK_ENV") == "development":
    MS_COMPRAS_URL = os.getenv("MS_COMPRAS_URL")
elif os.getenv("FLASK_ENV") == "testing":
    MS_COMPRAS_URL = os.getenv("MS_COMPRAS_TEST_URL")


class CompraService:
    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    @staticmethod
    def crear_compra(data):
        r = requests.post(f"{MS_COMPRAS_URL}/compras/", json=data)
        if r.status_code != 201:
            raise Exception("Error al crear la compra")
        else:
            data["compra_id"] = r.json()["id"]
            logging.info(f"Compra creada: {r.json()}")

    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    @staticmethod
    def compensar_compra(compra_id):
        try:
            r = requests.delete(f"{MS_COMPRAS_URL}/compras/{compra_id}")
            if r.status_code != 200:
                raise Exception("Error al compensar la compra")
            logging.info(f"Compra compensada: {r.json()}")
        except Exception as e:
            logging.error(f"Error al compensar la compra: {e}")
            raise
