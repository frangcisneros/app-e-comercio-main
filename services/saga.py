from pathlib import Path
from services.inventory_service import InventoryService
from services.compra_service import CompraService
from services.pago_service import crear_pago, compensar_pago
from saga import SagaBuilder, SagaError
from dotenv import load_dotenv
import os

basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, ".env"))


def saga_compra(data):
    saga_builder = SagaBuilder.create()

    saga_builder.action(
        action=lambda: CompraService.crear_compra(data),
        compensation=lambda: CompraService.compensar_compra(data["compra_id"]),
    ).action(
        action=lambda: crear_pago(data),
        compensation=lambda: compensar_pago(data["pago_id"]),
    ).action(
        action=lambda: InventoryService.inventory_sell(data),
        compensation=lambda: InventoryService.compensar_inventory_sell(data),
    )

    saga = saga_builder.build()
    try:
        saga.execute()
        print("Orden creada con éxito")
        return {"status": "Orden creada con éxito"}, 200
    except SagaError as e:
        print(f"Error al crear la orden: {e}")
        return {"status": "Error al crear la orden", "detail": str(e)}, 500
