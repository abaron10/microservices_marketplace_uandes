# Servicio de agenda

Por medio de este servicio, se pueden crear agendamientos entre un pedido y un proveedor. Es decir, solicitar a un proveedor que inicie la construcción de un pedido que ya está creado. Como parte de su funcionamiento es importante comprender:

- Un proveedor solo puede ejecutar un servicio al tiempo. Por lo tanto, si se le agenda un pedido, este lo aceptará, pero al tratar de agendar otro lanzará un error por no contar con disponibilidad para ejecutarlo.

A continuación, se indica cuales endpoints ofrece y las características de cada uno:

|||
| --- | --- |
| Componente | Agenda |
| Código | agenda |
| Método de consumo | REST |
| Despliegue | Contenedores sobre kubernetes |
| Propósito | Contiene las funcionalidades que permiten crear un agendamiento de un pedido para un proveedor, borrar el agendamiento y consultar el agendamiento |

## API

### Creación de agendamiento para un proveedor

* **Descripción**

|||
| --- | --- |
| Método | POST |
| Ruta | /agenda/sellers/:uuid |
| Parámetros | uuid: cadena de caracteres que representa el identificador del proveedor en el sistema. |
| Cuerpo |<code>{"uuid": uuid de la orden}</code> |

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 400 | | En el caso que el uuid enviado no sea correcto, o el cuerpo no lleve el uuid de la orden. |
| 412 | | En el caso que el pedido ya esté agendado para ese proveedor o el proveedor no tenga más disponibilidad para agendar. Para simular este fallo **agende 2 veces al proveedor, al segundo responderá que el proveedor no tiene disponibilidad**. |
| 201 | <code>{"sellerId": uuid del proveedor,"seller": ubicación del objeto proveedor,"orderId": uuid de la orden, "order": ubicación del objeto de la orden, "createdAt": fecha de creación del agendamiento, "state": estado, por defecto es 'requested'}</code>| En el caso que el pedido se agendó con éxito. |

### Consulta del agendamiento de una orden y un proveedor

* **Descripción**

|||
| --- | --- |
| Método | GET |
| Ruta | /agenda/sellers/:uuid/order/:ouuid |
| Parámetros | uuid: cadena de caracteres que representa el identificador del proveedor en el sistema.|
|            | ouuid: cadena de caracteres que representa el identificador de una orden en el sistema.|

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 400 | | En el caso que alguno de los uuids en la ruta no sean correctos. |
| 404 | | En el caso que no exista el agendamiento entre el proveedor y la orden. |
| 200 | <code>{"sellerId": uuid del proveedor,"seller": ubicación del objeto proveedor,"orderId": uuid de la orden, "order": ubicación del objeto de la orden, "createdAt": fecha de creación del agendamiento, "state": estado, por defecto es 'requested'}</code>| En el caso que el agendamiento del pedido exista. |

### Eliminar agendamiento de una orden y un proveedor

* **Descripción**

|||
| --- | --- |
| Método | DELETE |
| Ruta | /agenda/sellers/:uuid/order/:ouuid |
| Parámetros | uuid: cadena de caracteres que representa el identificador del proveedor en el sistema.|
|            | ouuid: cadena de caracteres que representa el identificador de una orden en el sistema.|

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 400 | | En el caso que alguno de los uuids en la ruta no sean correctos. |
| 404 | | En el caso que no exista el agendamiento entre el proveedor y la orden. |
| 200 | | En el caso que el agendamiento haya sido eliminado exitósamente. |

### Restablecer base de datos

> **Endpoint usado solo para testing**

* **Descripción**

|||
| --- | --- |
| Método | POST |
| Ruta | /agenda/reset |
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
| Ruta | /agenda/health/ping |

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 200 |  <code>pong</code> | Solo para confirmar que el servicio está arriba. |