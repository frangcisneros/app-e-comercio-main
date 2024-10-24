import requests
import logging

def inventory_sell(data):
    r = requests.post("http://localhost:5000/api/v1/stock/sell", json=data)
    if r.status_code != 200:
        print(r.json())
        raise Exception("Error al vender el producto")
    else:
        logging.info(r.json())


def compensar_inventory_sell(data):
    r = requests.post("http://localhost:5000/api/v1/stock/refuel", json=data)
    if r.status_code != 200:
        raise Exception("Error al compensar la venta del producto")
    else:
        logging.error(r.json())  