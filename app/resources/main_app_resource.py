from flask import Blueprint, jsonify, request
import requests
from services.orquestador import saga_compra

main_app_bp = Blueprint("main_app", __name__)


@main_app_bp.route("/saga/compra", methods=["POST"])
def saga_compra_endpoint():
    data = request.get_json()
    try:
        response, status_code = saga_compra(data)
    except Exception as e:
        return jsonify({"status": "Error al procesar la compra", "detail": str(e)}), 400
    return jsonify(response), status_code


@main_app_bp.route("/get_product/<int:id>", methods=["GET"])
def get_product(id):
    response = requests.get(f"http://localhost:5003/api/v1/get_product/{id}")
    return response.json(), response.status_code


@main_app_bp.route("/buy_product/<int:id>/<int:quantity>", methods=["POST"])
def buy_product(id, quantity):
    # obtener producto
    response_catalogo = requests.get(f"http://localhost:5003/api/v1/get_product/{id}")
    response_catalogo_data = response_catalogo.json()[0]
    # compra
    compra_data = {"producto_id": id, "direccion_envio": "Calle 2"}
    response_compra = requests.post(f"http://localhost:5001/compras/", json=compra_data)
    # pago
    compra_data = {
        "producto_id": id,
        "precio": response_catalogo_data["price"],
        "medio_pago": "tarjeta",
    }
    response_pago = requests.post(
        f"http://localhost:5002/api/v1/pago", json=compra_data
    )
    # inventario
    response_stock = requests.post(
        "http://localhost:5000/api/v1/stock/sell",
        json={"product_id": id, "quantity": quantity},
    )
    return response_stock.json(), response_stock.status_code
