from saga import Saga, SagaBuilder, SagaError
import requests

CATALOGO_SERVICE_URL = 'http://localhost:5003/api/v1/get_product/'
COMPRA_SERVICE_URL = 'http://localhost:5001/compras/'
PAGO_SERVICE_URL = 'http://localhost:5002/api/v1/pago'
INVENTARIO_SERVICE_URL = 'http://localhost:5000/api/v1/stock/sell'
ROLLBACK_CATALOGO_URL = 'http://inventory_service/rollback'
ROLLBACK_PAYMENT_URL = 'http://payment_service/rollback'

def crear_orden(data):
    saga_builder = SagaBuilder.create()

    # Paso : select producto
    saga_builder.action(
        action=lambda: requests.post(CATALOGO_SERVICE_URL, json=data),
        compensation=lambda: requests.post(ROLLBACK_CATALOGO_URL, json=data)
    )

    # Paso : Compra
    saga_builder.action(
        action=lambda: requests.post(COMPRA_SERVICE_URL, json=data),
        compensation=lambda: requests.post(COMPRA_SERVICE_URL + 'rollback', json=data)
    )

    # Paso 2: Procesar el pago
    saga_builder.action(
        action=lambda: requests.post(PAGO_SERVICE_URL, json=data),
        compensation=lambda: requests.post(PAGO_SERVICE_URL + '/rollback', json=data)
    )

    # Paso 3: INVENTARIO
    saga_builder.action(
        action=lambda: requests.post(INVENTARIO_SERVICE_URL, json=data),
        compensation=lambda: None  # No necesito rollback, es el paso final
    )

    saga = saga_builder.build()

    try:
    
        saga.execute()
        print("todo salio bien")
        return {"status": "Orden creada con éxito"}, 200
    except SagaError as e:
        print("algo no anda bien")
        return {"status": "Error al crear la orden", "detail": str(e)}, 500
