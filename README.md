# Microservicios proyecto Cloud Native segunda parte

En este repositorio se encuentran los archivos de despliegue y pruebas de los aplicaciones construidas como microservicios que son de uso obligatorio para la segunda entrega del proyecto.

## Contexto

En la actualidad contamos con 4 microservicios relacionados con la gestión de pedidos y pagos en la plataforma. Estos son:

- [Servicio de agenda](./agenda)
- [Servicio de pedidos](./orders)
- [Servicio de pagos](./payments)
- [Servicio de proveedores](./sellers)

El desafio es aprovechar estas cuatro aplicaciones, en conjunto con el monolito (la roca), y resolver dos requerimientos funcionales solicitados por la gerencia.

## Instrucciones

> Para evitar cualquier costo adicional en la nube, evite hacer despliegues hasta el momento en que inicie la configuración y pruebas de su entrega en el ambiente de nube.

### Ambiente local

Le recomendamos primero hacer un despliegue local para que pueda avanzar con el diseño de su arquitectura. Solo hasta que sea necesario continúe con los pasos para la publicación en K8s.

1. Clone este repositorio en su máquina.
2. En la raiz del proyecto encontrará un archivo de docker compose para ejecutar todo el grupo localmente. Revíselo para tener claridad en que puerto estará escuchando cada aplicación; 3020, 3030, 3040, 3050. Ejecute el siguiente comando para levantar a todas las contenedoras localmente.
```
docker-compose up
```
3. Para cada aplicación hay una carpeta en la que encontrará un archivo README con la documentación de la aplicación y una carpeta con el nombre **postman** la cual contiene un archivo de pruebas. Cargue los archivos en su cliente de postman.

|Imagen|Aplicación|Carpeta|
|---|---|---|
|agenda-service-p2:0.1.0|agenda|agenda/postman|
|orders-service-p2:0.1.0|orders|orders/postman|
|payments-service-p2:0.1.0|payments|payments/postman|
|sellers-service-p2:0.1.0|sellers|sellers/postman|

6. En postman modifique cada colección para que apunte al puerto correspondiente según la aplicación, y ejecute las pruebas.
5. A medida que ejecuta cada aplicación, acceda a la carpeta de cada aplicación y lea la documentación descrita en el README. En ella se describe el propósito, los endpoints que tiene y como es su funcionamiento.

### Ambiente Cloud

Dado que estas aplicaciones construidas como microservicios se comunicarán con el monolito desplegaremos todo en el mismo cluster.
>Postergue este despliegue hasta el punto en que realmente lo considere necesario.

1. En la raiz de este proyecto encontrará un archivo con el nombre **k8-deployments.yml**
```
kubectl apply -f k8-deployments.yml
```
4. Este archivo construirá toda la infraestructura necesaria para las 4 aplicaciones en k8s. Por lo que puede tardar un rato que quede desplegado.
5. Acceda a la consola de GCP y revise la ejecución de los servicios en **Kubernetes Engine > Ingress y servicios**.
6. Acceda a **Kubernetes Engine > Ingress y servicios > Entrada** y encontrará el único punto de entrada a todas las aplicaciones. Si lo desea, configure las colecciones de postman y pruebe con esa dirección IP.

## Puntos relevantes a tener en cuenta

Para que pueda realizar pruebas con las aplicaciones, en la carpeta **_data** encontrará un archivo con los identificadores de los productos que tienen asignado un proveedor en el sistema, y otro con los identificadores de los proveedores.

> **ATENCIÓN**: Los proyectos fueron creados con un objetivo académico y pedagógico, por lo que cada aplicación simula sus operaciones haciendo uso de una base de datos en memoria, se recomienda:
> 1. Siempre que realice pruebas con estas aplicaciones ejecute una solicitud post a la ruta **<APP>/reset** para mantener la base de datos limpia y evitar consumo excesivo de ram. Revise la documentación de cada aplicación.
> 2. No escale las aplicaciones o llevará a problemas de consistencia de la información.

## Sobre la resilencia

En ambos puntos del proyecto se debe simular fallos y configurar sus aplicaciones para que sean resilientes. Para cada punto hemos agregado formas en que pueden simular esos fallos.

1. Para el punto de creación de información, le recomendamos leer el README de cada aplicación para conocer bajo cuales condiciones se lanzan errores.
2. Para el punto de consumo de información, le recomendamos leer el contenido de la carpeta [resiliencia](./_resilience).

Utilice esta información para diseñar la estrategia con la que solucionará los requerimientos funcionales solicitados.

Éxitos!!