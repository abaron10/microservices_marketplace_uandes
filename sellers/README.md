# Servicio de proveedores

Por medio de este servicio, se pueden consultar los proveedores registrados en la plataforma. Se puede realizar la consulta por el identificador el proveedor o por medio del identificador del producto relacionado.

A continuación, se indica cuales endpoints ofrece y las características de cada uno:

|||
| --- | --- |
| Componente | Proveedores |
| Código | sellers |
| Método de consumo | REST |
| Despliegue | Contenedores sobre kubernetes |
| Propósito | Contiene las funcionalidades que permiten consultar un proveedor de la plataforma y su estado, así como consultar un proveedor por producto que vende. |

## API

### Consulta de proveedor por identificador

* **Descripción**

|||
| --- | --- |
| Método | GET |
| Ruta | /sellers/:uuid |
| Parámetros | uuid: cadena de caracteres que representa el identificador del proveedor en la base de datos. |

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 400 | | En el caso que el uuid enviado no sea correcto |
| 404 | | En el caso que el proveedor buscado no exista en la base de datos. |
| 200 | <code>{ "name": nombre,"nit":identificador tributario del proveedor., "uuid": uuid, "isActive": true-false}</code>| En el caso que el proveedor buscado exista en la base de datos. |

### Consulta de proveedor por producto

* **Descripción**

|||
| --- | --- |
| Método | GET |
| Ruta | /sellers/item/:uuid |
| Parámetros | uuid: cadena de caracteres que representa el identificador del producto en la base de datos. |

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 400 | | En el caso que el uuid enviado no sea correcto |
| 404 | | En el caso que no exista el proveedor dueño del producto. |
| 200 | <code>{ "name": nombre,"nit":identificador tributario del proveedor., "uuid": uuid, "isActive": true-false}</code>| En el caso que el proveedor buscado exista en la base de datos. |

### Consulta de salud del contenedor

* **Descripción**

|||
| --- | --- |
| Método | GET |
| Ruta | /sellers/health/ping |

* **Respuestas**

| Código | Cuerpo | Descripción |
| --- | --- | --- |
| 200 |  <code>pong </code> | Solo para confirmar que el servicio está arriba. |