import requests
import redis
import logging
import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

redis_url = os.getenv("REDIS_URL")
redis_client = redis.StrictRedis.from_url(redis_url)


def inventory_sell(data):
    product_id = data["product_id"]
    lock_key = f"lock:product:{product_id}"
    lock = redis_client.lock(lock_key, timeout=5)

    if not lock.acquire(blocking=False):
        raise Exception("No se pudo adquirir el bloqueo, reintentar la operación")

    try:
        session = Session()
        quantity = data["quantity"]

        # Verificar la cantidad de inventario disponible
        result = session.execute(
            text(
                "SELECT quantity FROM stock_schema.stock WHERE product_id = :product_id FOR UPDATE"
            ),
            {"product_id": product_id},
        ).fetchone()

        if result is None or result["quantity"] < quantity:
            raise Exception("Inventario insuficiente")

        # Actualizar el inventario
        session.execute(
            text(
                "UPDATE stock_schema.stock SET quantity = quantity - :quantity WHERE product_id = :product_id"
            ),
            {"quantity": quantity, "product_id": product_id},
        )

        session.commit()
        logging.info(f"Producto {product_id} vendido, cantidad: {quantity}")
        return {
            "status": "success",
            "message": f"Producto {product_id} vendido, cantidad: {quantity}",
        }
    except Exception as e:
        session.rollback()
        logging.error(f"Error al vender el producto: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        lock.release()
        session.close()


def compensar_inventory_sell(data):
    r = requests.post(f"{os.getenv("MS_STOCK_URL")}/api/v1/stock/refuel", json=data)
    if r.status_code != 200:
        raise Exception("Error al compensar la venta del producto")
    else:
        logging.error(r.json())
