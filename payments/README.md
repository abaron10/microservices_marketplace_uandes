# Servicio de pagos

Por medio de este servicio, se pueden crear pagos que serán ejecutados posteriormente de forma asíncrona. Para crear un pago es necesario contar con la información del pedido y el usuario que va a realizar el pago. Al mismo tiempo, es importante tener presente el límite de pagos:

- Con el fin de brindar seguridad en la plataforma, no está permitido que un usuario pueda realizar más de dos pagos consecutivos en la plataforma. En el caso que se presente, el sistema bloqueará el método de pago del usuario y lanzará error siempre que se quiera realizar un pago con ese usuario.

A continuación, se indica cuales endpoints ofrece y las características de cada uno:

|||
| --- | --- |
| Componente | Pagos |
| Código | payments |
| Método de consumo | REST |
| Despliegue | Contenedores sobre kubernetes |
| Propósito | Contiene las funcionalidades que permiten crear, borrar y consultar un pago.|


## API

### Creación de un pago

* **Descripción**

|||
| --- | --- |
| Método | POST |
| Ruta | /payments |
| Cuerpo |<code>{"order": {"uuid":"identificador del pedido a facturar"},"user": {"uuid": "identificador del usuario"}}</code> |

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 400 | | En el caso que el cuerpo no lleve los ids del pedido y del usuario. |
| 412 | <code>{"msg":"Método de pago bloqueado por seguridad"}</code>| En el caso en que el usuario haya realizado varios pagos consecutivos. Para simular este fallo, **ejecute 3 pagos con el mismo usuario, al tercero la cuenta se bloqueará**. |
| 412 | | En el caso que ya exista un pago activo asociado al pedido.|
| 201 | <code>{"orderId": "Identificador del pedido", "order": "Ubicación del objeto del pedido en el sistema","userId": "Identificador del usuario","user": "Ubicación del objeto del usuario en el sistema","paymentId": "Identificados del pago", "payment": "Ubicación del objeto del pago en el sistema","createdAt": "Fecha de creación del pago","state": "Estado del pago, por defecto processing"}</code>| En el caso que el pago se haya creado con éxito, y se haya solicitado proceder con el pago ante un tercero de manera asíncrona. |

### Consulta del pago

* **Descripción**

|||
| --- | --- |
| Método | GET |
| Ruta | /payments/:uuid |
| Parámetros | uuid: cadena de caracteres que representa el identificador del pago.|

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 400 | | En el caso que el uuid en la ruta no sea correcto. |
| 404 | | En el caso que no exista un pago con ese uuid. |
| 200 | <code>{"orderId": "Identificador del pedido", "order": "Ubicación del objeto del pedido en el sistema","userId": "Identificador del usuario","user": "Ubicación del objeto del usuario en el sistema","paymentId": "Identificador del pago", "payment": "Ubicación del objeto del pago en el sistema","createdAt": "Fecha de creación del pago","state": "Estado del pago, por defecto processing"}</code>| Si el pago existe. |

### Consulta del pago por pedido

* **Descripción**

|||
| --- | --- |
| Método | GET |
| Ruta | /orders/:uuid |
| Parámetros | uuid: cadena de caracteres que representa el identificador del pedido.|

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 400 | | En el caso que el uuid en la ruta no sea correcto.|
| 404 | | En el caso que no exista un pago asociado a un pedido con ese uuid. |
| 200 | <code>{"orderId": "Identificador del pedido", "order": "Ubicación del objeto del pedido en el sistema","userId": "Identificador del usuario","user": "Ubicación del objeto del usuario en el sistema","paymentId": "Identificador del pago", "payment": "Ubicación del objeto del pago en el sistema","createdAt": "Fecha de creación del pago","state": "Estado del pago, por defecto processing"}</code>| Si el pago asociado al pedido existe. |

### Eliminar pedido

* **Descripción**

|||
| --- | --- |
| Método | DELETE |
| Ruta | /payments/:uuid |
| Parámetros | uuid: cadena de caracteres que representa el identificador del pago.|

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 400 | | En el caso que el uuid en la ruta no sea correcto. |
| 404 | | En el caso que no exista un pago con ese identificador. |
| 200 | | En el caso que el pago haya sido eliminado exitósamente. Este paso implica que otra tarea asíncrona será creada para cancelar la transacción con la plataforma de pagos. |

### Restablecer base de datos

> **Endpoint usado solo para testing**

* **Descripción**

|||
| --- | --- |
| Método | POST |
| Ruta | /payments/reset |
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
| Ruta | /payments/health/ping |

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 200 |  <code>pong</code> | Solo para confirmar que el servicio está arriba. |