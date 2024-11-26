import logging
import requests


def crear_pago(data):
    r = requests.post("http://localhost:5002/api/v1/pago", json=data)
    if r.status_code != 201:
        raise Exception("Error al crear el pago")
    else:
        data["pago_id"] = r.json()["id"]
        logging.info(r.json())


def compensar_pago(pago_id):
    r = requests.delete(f"http://localhost:5002/api/v1/pago/eliminar/{pago_id}")
    if r.status_code != 200:
        raise Exception("Error al compensar el pago")
    else:
        logging.error(r.json())
