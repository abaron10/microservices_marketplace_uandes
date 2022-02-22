from flask import Blueprint, request, Response
from injector import inject
import requests
import json
import os
import pybreaker

pedido_api = Blueprint('pedido_api', __name__)
ORDERS_PATH = os.environ["ORDERS_PATH"]
AGENDA_PATH = os.environ["AGENDA_PATH"]
PAYMENTS_PATH = os.environ["PAYMENTS_PATH"]
SELLERS_PATH = os.environ["SELLERS_PATH"]
MONOLITH_PATH = os.environ["MONOLITH_PATH"]
FAILURES = 1
TIMEOUT = 6

circuitOrder = pybreaker.CircuitBreaker(fail_max=FAILURES, reset_timeout=TIMEOUT)
circuitAgenda = pybreaker.CircuitBreaker(fail_max=FAILURES, reset_timeout=TIMEOUT)
circuitPago = pybreaker.CircuitBreaker(fail_max=FAILURES, reset_timeout=TIMEOUT)
circuitProveedor = pybreaker.CircuitBreaker(fail_max=FAILURES, reset_timeout=TIMEOUT)


def create_order(data):
    @circuitOrder
    def create_order_post():
        order_response = requests.post(f"{ORDERS_PATH}/orders", json=data, timeout=2)
        if order_response.status_code == 201:
            return 201,order_response
        else:
            return 503,order_response.json()
    try:
        return create_order_post()
    except:
        return 408,"TimeOut para el servicio de ordenes"

def get_order(pedido_id):
    @circuitOrder
    def get_order_get():
        order_response = requests.get(f"{ORDERS_PATH}/orders/{pedido_id}", timeout=2)
        if order_response.status_code == 201:
            return 201,order_response
        else:
            return order_response.status_code,order_response.json()
    try:
        return get_order_get()
    except:
        return 408,"TimeOut para el servicio de ordenes"

def create_agenda(order_id, seller_id, agenda_data):
    @circuitAgenda
    def create_agenda_post():
        agenda_response = requests.post(f"{AGENDA_PATH}/agenda/sellers/{seller_id}", json=agenda_data, timeout=2)
        if agenda_response.status_code == 201:
            return 201,agenda_response
        else:
            requests.delete(f"{ORDERS_PATH}/orders/{order_id}")
            return 412,agenda_response.json()
    try:
        return create_agenda_post()
    except:
        requests.delete(f"{ORDERS_PATH}/orders/{order_id}")
        return 408,"TimeOut para el servicio de agenda"

def get_agenda(seller_id, pedido_id):
    @circuitAgenda
    def get_agenda_get():
        agenda_response = requests.get(f"{AGENDA_PATH}/agenda/sellers/{seller_id}/order/{pedido_id}", timeout=2)
        if agenda_response.status_code == 201:
            return 201,agenda_response
        else:
            return agenda_response.status_code,agenda_response.json()
    try:
        return get_agenda_get()
    except:
        return 408,"TimeOut para el servicio de agenda"     

def create_pago(order_id, seller_id, pago_data):
    @circuitPago
    def create_pago_post():
        pago_response = requests.post(f"{PAYMENTS_PATH}/payments", json=pago_data, timeout=2)
        if pago_response.status_code == 201:
            return 201,pago_response
        else:
            requests.delete(f"{AGENDA_PATH}/agenda/sellers/{seller_id}/order/{order_id}")
            requests.delete(f"{ORDERS_PATH}/orders/{order_id}")
            return 412,pago_response.json()
    try:
        return create_pago_post()
    except:
        requests.delete(f"{AGENDA_PATH}/agenda/sellers/{seller_id}/order/{order_id}")
        requests.delete(f"{ORDERS_PATH}/orders/{order_id}")
        return 408,"TimeOut para el servicio de pagos"

def get_pago(pedido_id):
    @circuitPago
    def get_pago_get():
        pago_response = requests.get(f"{PAYMENTS_PATH}/payments/orders/{pedido_id}", timeout=2)
        if pago_response.status_code == 201:
            return 201,pago_response
        else:
            return pago_response.status_code,pago_response.json()
    try:
        return get_pago_get()
    except:
        return 408,"TimeOut para el servicio de pagos"

def get_seller(seller_id):
    @circuitProveedor
    def get_seller_get():
        seller_response = requests.get(f"{SELLERS_PATH}/sellers/{seller_id}", timeout=2)
        if seller_response.status_code == 201:
            return 201,seller_response
        else:
            return seller_response.status_code,seller_response.json()
    try:
        return get_seller_get()
    except:
        return 408,"TimeOut para el servicio de proveedores"

def esta_abierto(circuit, name):
    if circuit._state_storage.state == 'open':
        print("Servicio de ", name, " estado del circuit0: ", circuit._state_storage.state)
        return True,"Servicio de "+name+" temporalmente indisponible"
    else:
        print("Servicio de ", name, " estado del circuito: ", circuit._state_storage.state)
        return False,""

@inject
@pedido_api.route('/', methods=['POST'])
def crear_pedido():
    token = request.headers["x-auth-token"]

    validation_login = requests.get(f"{MONOLITH_PATH}/sesion/{token}")

    if validation_login.status_code != 200:
        return validation_login.json(), 401

    data = request.get_json()
    item_id = data["item"]["uuid"]
    exist_product = requests.get(f"{MONOLITH_PATH}/producto/{item_id}")

    if exist_product.status_code != 200:
        return exist_product.json(),404

    cod_rta,order_response = create_order(data)
    if cod_rta != 201:
        cbabierto,mensaje = esta_abierto(circuitOrder, "ordenes")
        if cbabierto:        
            return Response(f'{{"mensaje":"{mensaje}"}}', status=503, mimetype='application/json')
        if cod_rta == 408:
            return Response(f'{{"mensaje":"{order_response}"}}', status=cod_rta, mimetype='application/json')
        return order_response,cod_rta

    order_id = order_response.json()["orderId"]
    user_id = order_response.json()["userId"]
    seller_id = order_response.json()["sellerId"]
    agenda_data = { "uuid": order_id }
    
    cod_rta,agenda_response = create_agenda(order_id, seller_id, agenda_data)
    if cod_rta != 201:
        cbabierto,mensaje = esta_abierto(circuitAgenda, "agenda")
        if cbabierto:        
            return Response(f'{{"mensaje":"{mensaje}"}}', status=503, mimetype='application/json')
        if cod_rta == 408:
            return Response(f'{{"mensaje":"{agenda_response}"}}', status=cod_rta, mimetype='application/json')
        return agenda_response,cod_rta

    pago_data = { "order": { "uuid": order_id }, "user": { "uuid": user_id } }
    cod_rta,pago_response = create_pago(order_id, seller_id, pago_data) 
    if cod_rta != 201:
        cbabierto,mensaje = esta_abierto(circuitPago, "pagos")
        if cbabierto:        
            return Response(f'{{"mensaje":"{mensaje}"}}', status=503, mimetype='application/json')
        if cod_rta == 408:
            return Response(f'{{"mensaje":"{pago_response}"}}', status=cod_rta, mimetype='application/json')
        return pago_response,cod_rta   

    print(f"{order_id}")
    return order_response.json(), 200

@inject
@pedido_api.route('/<pedido_id>', methods=['GET'])
def dar_pedido(pedido_id: int):
    token = request.headers["x-auth-token"] 
    validation_login = requests.get(f"{MONOLITH_PATH}/sesion/{token}")
    if validation_login.status_code != 200:
        return validation_login.json(), 401

    cod_rta,order_response = get_order(pedido_id)
    if cod_rta != 201:
        cbabierto,mensaje = esta_abierto(circuitOrder, "ordenes")
        if cbabierto:        
            return Response(f'{{"mensaje":"{mensaje}"}}', status=503, mimetype='application/json')
        if cod_rta == 408:
            return Response(f'{{"mensaje":"{order_response}"}}', status=cod_rta, mimetype='application/json')
        return order_response,cod_rta

    seller_id = order_response.json()["sellerId"]
    item_id = order_response.json()["itemId"]

    cod_rta,agenda_response = get_agenda(seller_id, pedido_id) 
    if cod_rta != 201:
        cbabierto,mensaje = esta_abierto(circuitAgenda, "agenda")
        if cbabierto:        
            return Response(f'{{"mensaje":"{mensaje}"}}', status=503, mimetype='application/json')
        if cod_rta == 408:
            return Response(f'{{"mensaje":"{agenda_response}"}}', status=cod_rta, mimetype='application/json')
        return agenda_response,cod_rta

    cod_rta,pago_response = get_pago(pedido_id) 
    if cod_rta != 201:
        cbabierto,mensaje = esta_abierto(circuitPago, "pagos")
        if cbabierto:        
            return Response(f'{{"mensaje":"{mensaje}"}}', status=503, mimetype='application/json')
        if cod_rta == 408:
            return Response(f'{{"mensaje":"{pago_response}"}}', status=cod_rta, mimetype='application/json')
        return pago_response,cod_rta 

    cod_rta,seller_response = get_seller(seller_id)
    if cod_rta != 201:
        cbabierto,mensaje = esta_abierto(circuitProveedor, "proveedores")
        if cbabierto:        
            return Response(f'{{"mensaje":"{mensaje}"}}', status=503, mimetype='application/json')
        if cod_rta == 408:
            return Response(f'{{"mensaje":"{seller_response}"}}', status=cod_rta, mimetype='application/json')
        return seller_response,cod_rta

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
