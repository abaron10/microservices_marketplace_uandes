from flask import Blueprint, request
from injector import inject

pedido_api = Blueprint('pedido_api', __name__)

@inject
@pedido_api.route('/', methods=['POST'])
def crear_pedido():
    return { "message": "Crear" }, 200

@inject
@pedido_api.route('/<pedido_id>', methods=['GET'])
def dar_pedido(pedido_id: int):
    return { "message": "Detalle" }, 200