from saga import Saga, SagaBuilder, SagaError
from services.compra_service import CompraService
from services.pago_service import crear_pago, compensar_pago
from services.inventory_service import inventory_sell


def saga_compra(data):
    saga_builder = SagaBuilder.create()

    saga_builder.action(
        action=lambda: CompraService.crear_compra(data),
        compensation=lambda: CompraService.compensar_compra(data["compra_id"])
    ).action(
        action=lambda: crear_pago(data),
        compensation=lambda: compensar_pago(data["pago_id"])
    ).action(
        action=lambda: inventory_sell(data),
        compensation=lambda: None
    )

    saga = saga_builder.build()
    try:
        saga.execute()
        return {"status": "Orden creada con éxito"}, 200
    except SagaError as e:
        print("algo no anda bien")
        return {"status": "Error al crear la orden", "detail": str(e)}, 500
