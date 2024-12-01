import logging
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, ".env"))


def crear_pago(data):
    try:
        r = requests.post(f"{os.getenv('MS_PAGO_URL')}/api/v1/pago", json=data)
        if r.status_code != 201:
            raise Exception("Error al crear el pago")
        else:
            data["pago_id"] = r.json()["id"]
            logging.info(f"Pago creado: {r.json()}")
    except Exception as e:
        logging.error(f"Error al crear el pago: {e}")
        raise


def compensar_pago(pago_id):
    try:
        r = requests.delete(
            f"{os.getenv('MS_PAGO_URL')}/api/v1/pago/eliminar/{pago_id}"
        )
        if r.status_code != 200:
            raise Exception("Error al compensar el pago")
        logging.info(f"Pago compensado: {r.json()}")
    except Exception as e:
        logging.error(f"Error al compensar el pago: {e}")
        raise
