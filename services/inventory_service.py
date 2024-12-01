from app import db
from sqlalchemy import text
import requests
import redis
import logging
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, ".env"))

DATABASE_URL = os.getenv("DATABASE_PROD_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

redis_url = os.getenv("REDIS_URL")
if redis_url is None:
    raise ValueError("REDIS_URL environment variable is not set")
redis_client = redis.StrictRedis.from_url(redis_url)


def check_quantity(product_id):
    session = Session()
    result = (
        session.execute(
            text(
                "SELECT SUM(CASE WHEN in_out = 'in' THEN quantity ELSE -quantity END) AS balance FROM stock_schema.stock WHERE product_id = :product_id"
            ),
            {"product_id": product_id},
        )
        .mappings()
        .fetchone()
    )
    session.close()
    return result["balance"] if result else 0


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
        balance = check_quantity(product_id)

        if balance < quantity:
            raise Exception("Inventario insuficiente")

        # Registrar la salida del inventario
        session.execute(
            text(
                "INSERT INTO stock_schema.stock (product_id, quantity, in_out) VALUES (:product_id, :quantity, 'out')"
            ),
            {"product_id": product_id, "quantity": quantity},
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
