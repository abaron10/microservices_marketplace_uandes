# Servicio pedidos

Por medio de este servicio, se pueden crear pedidos en la plataforma. Para poder crear un pedido se requiere el producto que se desea comprar, quien es el proveedor y quien es el usuario que está por realizar la compra.

A continuación, se indica cuales endpoints ofrece y las características de cada uno:

|||
| --- | --- |
| Componente | Pedidos |
| Código | orders |
| Método de consumo | REST |
| Despliegue | Contenedores sobre kubernetes |
| Propósito | Contiene las funcionalidades que permiten crear, borrar y consultar un pedido |


## API

### Creación de un pedido

* **Descripción**

|||
| --- | --- |
| Método | POST |
| Ruta | /orders |
| Cuerpo |<code>{"item": {"uuid":"identificador del producto"},"seller": {"uuid": "identificador del proveedor"},"user": {"uuid": "identificador del usuario"}}</code> |

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 400 | | En el caso que el cuerpo no lleve los ids del producto, del proveedor o del usuario. |
| 201 | <code>{"sellerId": "identificador del proveedor","seller": "Ubicación del objeto proveedor en el sistema","userId": "identificador del usuario", "user": "Ubicación del objeto usuario en el sistema","itemId": "identificador del producto","item": "Ubicación del producto en el sistema","orderId": "identificador del pedido","order": "Ubicación del pedido en el sistema","createdAt": "fecha de creación del pedido","state": "estado del pedido, por defecto processing"}</code>| En el caso que el pedido se haya creado con éxito. |

### Consulta del pedido

* **Descripción**

|||
| --- | --- |
| Método | GET |
| Ruta | /orders/:uuid |
| Parámetros | uuid: cadena de caracteres que representa el identificador del pedido.|

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 400 | | En el caso que el uuid en la ruta no sea correcto. |
| 404 | | En el caso que no exista un pedido con ese uuid. |
| 200 | <code>{"sellerId": "identificador del proveedor","seller": "Ubicación del objeto proveedor en el sistema","userId": "identificador del usuario", "user": "Ubicación del objeto usuario en el sistema","itemId": "identificador del producto","item": "Ubicación del producto en el sistema","orderId": "identificador del pedido","order": "Ubicación del pedido en el sistema","createdAt": "fecha de creación del pedido","state": "estado del pedido, por defecto processing"}</code>| En el caso que el pedido exista. |

### Eliminar pedido

* **Descripción**

|||
| --- | --- |
| Método | DELETE |
| Ruta | /orders/:uuid |
| Parámetros | uuid: cadena de caracteres que representa el identificador del pedido.|

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 400 | | En el caso que el uuid en la ruta no sea correcto. |
| 404 | | En el caso que no exista un pedido con ese uuid. |
| 200 | | En el caso que el pedido haya sido eliminado exitósamente. |

### Restablecer base de datos

> **Endpoint usado solo para testing**

* **Descripción**

|||
| --- | --- |
| Método | POST |
| Ruta | /orders/reset |
| Cuerpo | No requiere |

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 200 || La base de datos ha sido reestablecida. |

### Consulta de salud del contenedor

* **Descripción**

|||
| --- | --- |
| Método | GET |
| Ruta | /orders/health/ping |

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 200 |  <code>pong</code> | Solo para confirmar que el servicio está arriba. |