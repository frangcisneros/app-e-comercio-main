from saga import Saga, SagaBuilder, SagaError
import requests
import json


def crear_compra(data):
    r = requests.post("http://localhost:5001/compras/", json=data)
    if r.status_code != 201:
        raise Exception("Error al crear la compra")
    else:
        data["compra_id"] = r.json()["id"]
        print(r.json())


def compensar_compra(compra_id):
    r = requests.delete(f"http://localhost:5001/compras/{compra_id}")
    if r.status_code != 200:
        raise Exception("Error al compensar la compra")
    else:
        print(r.json())


def crear_pago(data):
    r = requests.post("http://localhost:5002/api/v1/pago", json=data)
    if r.status_code != 201:
        raise Exception("Error al crear el pago")
    else:
        data["pago_id"] = r.json()["id"]
        print(r.json())


def compensar_pago(pago_id):
    r = requests.delete(f"http://localhost:5002/api/v1/pago/eliminar/{pago_id}")
    if r.status_code != 200:
        raise Exception("Error al compensar el pago")
    else:
        print(r.json())


def inventory_sell(data):
    r = requests.post("http://localhost:5000/api/v1/stock/sell", json=data)
    if r.status_code != 200:
        print(r.json())
        raise Exception("Error al vender el producto")
    else:
        print(r.json())


def compensar_inventory_sell(data):
    r = requests.post("http://localhost:5000/api/v1/stock/refuel", json=data)
    if r.status_code != 200:
        raise Exception("Error al compensar la venta del producto")
    else:
        print(r.json())


def saga_compra(data):
    saga_builder = SagaBuilder.create()
    # Paso : Compra
    saga_builder.action(
        action=lambda: crear_compra(data),
        compensation=lambda: compensar_compra(data["compra_id"]),
    )
    # Paso 2: Procesar el pago
    saga_builder.action(
        action=lambda: crear_pago(data),
        compensation=lambda: compensar_pago(data["pago_id"]),
    )
    # Paso 3: INVENTARIO
    saga_builder.action(
        action=lambda: inventory_sell(data),
        compensation=lambda: None,
    )
    # Ejecutar la saga
    saga = saga_builder.build()
    try:
        saga.execute()
        return {"status": "Orden creada con éxito"}, 200
    except SagaError as e:
        print("algo no anda bien")
        return {"status": "Error al crear la orden", "detail": str(e)}, 500
