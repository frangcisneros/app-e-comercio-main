import logging
import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from app import cache
from tenacity import retry, stop_after_attempt, wait_random


basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, ".env"))

@retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
def crear_pago(data):
    r = requests.post(f"{os.getenv("MS_PAGO_URL")}/api/v1/pago", json=data)
    if r.status_code != 201:
        raise Exception("Error al crear el pago")
    else:
        data["pago_id"] = r.json()["id"]
        logging.info(r.json())

@retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
def compensar_pago(pago_id):
    r = requests.delete(f"{os.getenv("MS_PAGO_URL")}/api/v1/pago/eliminar/{pago_id}")
    if r.status_code != 200:
        raise Exception("Error al compensar el pago")
    else:
        logging.error(r.json())
