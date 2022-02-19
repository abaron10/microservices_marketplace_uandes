from flask import Blueprint, request
from injector import inject
import requests
import json
import os
import pybreaker
import datetime

pedido_api = Blueprint('pedido_api', __name__)
ORDERS_PATH = os.environ["ORDERS_PATH"]
AGENDA_PATH = os.environ["AGENDA_PATH"]
PAYMENTS_PATH = os.environ["PAYMENTS_PATH"]
SELLERS_PATH = os.environ["SELLERS_PATH"]
MONOLITH_PATH = os.environ["MONOLITH_PATH"]

FAILURES = 3
TIMEOUT = 6
circuit = pybreaker.CircuitBreaker(fail_max=FAILURES, reset_timeout=TIMEOUT, name="get_greeting")


def user_session_validation(token):
    @circuit
    def auth_validation():
        validation_login = requests.get(f"{MONOLITH_PATH}/sesion/{token}")
        if validation_login.status_code != 200:
            return validation_login.json(), 401 
    try:
        return auth_validation()
    except:
        pass

def product_validation(item_id):
    @circuit
    def product_existance():
        exist_product = requests.get(f"{MONOLITH_PATH}/producto/{item_id}")
        if exist_product.status_code != 200:
            return exist_product.json(),404
    try:
        return product_existance()
    except:
        pass

def create_order(data):
    @circuit
    def create_order_post():
        order_response = requests.post(f"{ORDERS_PATH}/orders", json=data)
        if order_response.status_code != 201:
            return order_response.json(),503
        else:
            return order_response
    try:
        return create_order_post()
    except:
        pass

def book_order(seller_id, agenda_data, order_id):
    @circuit
    def book_order_validation():
        agenda_response = requests.post(f"{AGENDA_PATH}/agenda/sellers/{seller_id}", json=agenda_data)
        if agenda_response.status_code != 201:
            requests.delete(f"{ORDERS_PATH}/orders/{order_id}")
            return agenda_response.json(),412

        try:
            book_order_validation()
        except:
            pass    


@inject
@pedido_api.route('/', methods=['POST'])
def crear_pedido():
    data = request.get_json()
    item_id = data["item"]["uuid"]
    
    user_session_validation(request.headers["x-auth-token"])
    product_validation(item_id) 

    order_response = create_order(data)

    order_id = order_response.json()["orderId"]
    user_id = order_response.json()["userId"]
    seller_id = order_response.json()["sellerId"]
    agenda_data = { "uuid": order_id }
    book_order(seller_id,agenda_data,order_id)

    pago_data = { "order": { "uuid": order_id }, "user": { "uuid": user_id } }
    pago_response = requests.post(f"{PAYMENTS_PATH}/payments", json=pago_data)

    if pago_response.status_code != 201:
        requests.delete(f"{AGENDA_PATH}/agenda/sellers/{seller_id}/order/{order_id}")
        requests.delete(f"{ORDERS_PATH}/orders/{order_id}")
        return pago_response.json(),412
    print(f"{order_id}")
    print(print_summary())
    return order_response.json(), 200

@inject
@pedido_api.route('/<pedido_id>', methods=['GET'])
def dar_pedido(pedido_id: int):
    token = request.headers["x-auth-token"] 
    validation_login = requests.get(f"{MONOLITH_PATH}/sesion/{token}")
    if validation_login.status_code != 200:
        return validation_login.json(), 401

    order_response = requests.get(f"{ORDERS_PATH}/orders/{pedido_id}")
    seller_id = order_response.json()["sellerId"]
    item_id = order_response.json()["itemId"]
    agenda_response = requests.get(f"{AGENDA_PATH}/agenda/sellers/{seller_id}/order/{pedido_id}")
    pago_response = requests.get(f"{PAYMENTS_PATH}/payments/orders/{pedido_id}")
    seller_response = requests.get(f"{SELLERS_PATH}/sellers/{seller_id}")
    item_response = requests.get(f"{MONOLITH_PATH}/producto/{item_id}")

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
    requests.post(f"{ORDERS_PATH}/orders/reset")
    requests.post(f"{AGENDA_PATH}/agenda/reset")
    requests.post(f"{PAYMENTS_PATH}/payments/reset")
    return "OK", 200

def print_summary():
    name = circuit.name
    state = circuit._state_storage.state
    time_left = TIMEOUT
    if circuit._state_storage.opened_at:
        elapse_time = datetime.datetime.utcnow() - circuit._state_storage.opened_at
        time_left = TIMEOUT - elapse_time.total_seconds()
    print("{} circuit state: {}. Time till open: {}".format(name, state, time_left))