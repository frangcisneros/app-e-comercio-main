from saga import Saga, SagaBuilder, SagaError
from services.compra_service import CompraService
from services.pago_service import crear_pago, compensar_pago
from services.inventory_service import inventory_sell


import os
from dotenv import load_dotenv
from pathlib import Path


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
        action=lambda: inventory_sell(data), compensation=lambda: None
    )

    saga = saga_builder.build()
    try:
        saga.execute()
        print("Orden creada con éxito")
        return {"status": "Orden creada con éxito"}, 200
    except SagaError as e:
        print(f"algo no anda bien {e}")
        return {"status": "Error al crear la orden", "detail": str(e)}, 500
