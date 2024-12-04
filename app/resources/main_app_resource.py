from flask import Blueprint, jsonify, request
import requests
from services.saga import saga_compra

main_app_bp = Blueprint("main_app", __name__)

# TODO: pasarle las rutas a traves de env, mejor hacerlo cuando ponga los ms en gunicorn que voy a poder acceder a traves de rutas normales


@main_app_bp.route("/", methods=["GET"])
def hola_mundo():
    return jsonify({"message": "Hola Mundo!"})


@main_app_bp.route("/saga/compra", methods=["POST"])
def saga_compra_endpoint():
    data = request.get_json()
    try:
        response, status_code = saga_compra(data)
    except Exception as e:
        return jsonify({"status": "Error al procesar la compra", "detail": str(e)}), 400
    return jsonify(response), status_code
