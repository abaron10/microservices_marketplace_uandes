from flask import Blueprint, request
from injector import inject
import requests
import json

pedido_api = Blueprint('pedido_api', __name__)

@inject
@pedido_api.route('/', methods=['POST'])
def crear_pedido():
    data = request.get_json()
    # TODO: Validar autenticacion
    # TODO: Validar que exista el producto
    order_response = requests.post("http://localhost:3030/orders", json=data)
    order_id = order_response.json()["orderId"]
    user_id = order_response.json()["userId"]
    seller_id = order_response.json()["sellerId"]
    agenda_data = { "uuid": order_id }
    agenda_response = requests.post("http://localhost:3020/agenda/sellers/" + seller_id, json=agenda_data)
    # TODO: Mandar error si no tiene disponibilidad
    pago_data = { "order": { "uuid": order_id }, "user": { "uuid": user_id } }
    pago_response = requests.post("http://localhost:3040/payments", json=pago_data)
    return order_response.json(), 200

@inject
@pedido_api.route('/<pedido_id>', methods=['GET'])
def dar_pedido(pedido_id: int):
    order_response = requests.get("http://localhost:3030/orders/" + pedido_id)
    seller_id = order_response.json()["sellerId"]
    item_id = order_response.json()["itemId"]
    agenda_response = requests.get("http://localhost:3020/agenda/sellers/" + seller_id + "/order/" + pedido_id)
    pago_response = requests.get("http://localhost:3040/payments/orders/" + pedido_id)
    seller_response = requests.get("http://localhost:3050/sellers/" + seller_id)
    item_response = requests.get("http://localhost:3060/producto/" + item_id)

    agenda_json = agenda_response.json()
    pago_json = pago_response.json()
    seller_json = seller_response.json()
    item_json = item_response.json()
    return {
        "product": item_json,
        "agenda": {
            "createdAt": agenda_json["createdAt"],
            "state": agenda_json["state"]
        },
        "seller": seller_json,
        "payment": {
            "createdAt": pago_json["createdAt"],
            "state": pago_json["state"],
        }
    }, 200

@inject
@pedido_api.route('/health/ping', methods=['GET'])
def ping():
    return "pong", 200

@inject
@pedido_api.route('/reset', methods=['POST'])
def reset():
    requests.post("http://localhost:3030/orders/reset").text
    requests.post("http://localhost:3020/agenda/reset").text
    requests.post("http://localhost:3040/payments/reset").text
    return "OK", 200
