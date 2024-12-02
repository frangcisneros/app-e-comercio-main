import logging
import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_random
import redis

basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, ".env"))

redis_url = os.getenv("REDIS_URL")
if redis_url is None:
    raise ValueError("REDIS_URL environment variable is not set")
redis_client = redis.StrictRedis.from_url(redis_url)


class InventoryService:
    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    @staticmethod
    def check_quantity(product_id):
        response = requests.get(
            f"{os.getenv('MS_STOCK_URL')}/api/v1/stock/check_quantity/{product_id}"
        )
        if response.status_code != 200:
            raise Exception("Error al verificar la cantidad de inventario")
        elif response.status_code == 409:
            raise Exception("Stock insuficiente")
        return response.json()["quantity"]

    @staticmethod
    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    def inventory_sell(data):
        product_id = data["product_id"]
        lock_key = f"lock:product:{product_id}"
        lock = redis_client.lock(lock_key, timeout=5)

        if not lock.acquire(blocking=False):
            raise Exception("No se pudo adquirir el bloqueo, reintentar la operación")

        try:
            quantity = data["quantity"]

            # Verificar la cantidad de inventario disponible
            balance = InventoryService.check_quantity(product_id)
            logging.info(f"Cantidad de inventario antes de la venta: {balance}")

            # si el inventario es insuficiente, lanzar una excepción y un error 409
            if balance < quantity:
                logging.error("Inventario insuficiente")
                raise Exception("Inventario insuficiente")

            # Registrar la salida del inventario en el microservicio de stock
            response = requests.post(
                f"{os.getenv('MS_STOCK_URL')}/api/v1/stock/sell", json=data
            )
            if response.status_code != 200:
                raise Exception("Error al vender el producto")

            response_json = response.json()
            logging.info(f"Respuesta del microservicio de stock: {response_json}")

            # Verificar la cantidad de inventario después de la venta
            new_balance = InventoryService.check_quantity(product_id)
            logging.info(f"Cantidad de inventario después de la venta: {new_balance}")

            return response_json
        except Exception as e:
            logging.error(f"Error al vender el producto: {e}")
            raise
        finally:
            lock.release()

    @staticmethod
    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    def compensar_inventory_sell(data):
        pass
