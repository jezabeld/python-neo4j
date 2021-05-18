# python-neo4j

Este proyecto se creó para servir de práctica de los conceptos aprendidos en la Diplomatura en Arquitecturas de Big Data Aplicadas de la UTN, además de ser de utilidad para incorporar distintos conceptos y buenas prácticas del desarrollo de software.

Link a la info de la diplomatura:
https://sceu.frba.utn.edu.ar/course/diplomatura-en-arquitecturas-de-big-data-aplicadas/

El primer módulo cursado es el de Neo4j y Cassandra: https://sceu.frba.utn.edu.ar/course/big-data-nosql-cassandra-neo4j/

## De donde vengo y qué hago aquí
Mis conocimientos actuales abarcan conceptos generales de programación (con experiencia de varios años en R y stata, algo de python y muy poco de PHP, Perl, Lua, Visual Basic, C++). Me desempeñé varios años como Data Analyst y actualmente me encuentro dando mis primeros pasos como Data Engineer. 

En la educación formal obtuve únicamente el título secundario como Técnico Químico y actualmente me encuetro en la recta final de la carrera de Licenciatura en Estadística (a 2 finales de recibirme).

Este año (2021) me propuse una fuerte capacitación en varias ramas, incluyendo cuestiones generales de Big Data, Cloud Data Engineering y desarrollo. En esa linea surgió la idea de hacer este pequeño proyecto de la mano de gente que se dedica al Sofware Development hace varios años, para aprender los conceptos impartidos en las capacitaciones y muchos más que me sirvan para crecer profesionalmente.

Mi idea es ir comentando los distintos conceptos que iré aprendiendo sobre desarrollo de aplicaciones a medida que me voy encontrando con las diferentes problemáticas que implica la creación de un servicio desde cero (y sin conocimientos previos :P ).
___
## **1. Conceptos iniciales**
Dado que la idea fue desarrollar un servicio en python que utilizara la base de grafos Neo4j que estamos aprendiendo en el primer módulo de la diplomatura, fue necesario entender un poco sobre conceptos básicos de servicios REST:
- Qué es un *servicio*
- Métodos de comunicación entre aplicaciones
    - SOAP
    - RCP
    - gRCP
- REST como alternativa en la web 2.0
    - protocolo HTTP (request-response)
    - concepto de *stateless*
- *Endpoints* y *APIs*
- CRUD
- Arquitecturas orientadas a microservicios

## **2. Repaso de conceptos generales del uso de Git y GitHub**
El siguiente paso fue setear todo lo necesario en GIT, crear el repo nuevo python-neo4j y repasar los comando básicos para su uso.

## **3. Flask: framework web para python**
En la búsqueda de frameworks web para python surgió Flask como la alternativa más popular en la web.

https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application

## **4. Containers - Docker**
Un par de videos de intro a Docker y containers fueron suficientes para la creación del primer dockerfile para la app en python.

https://hub.docker.com/_/python

Luego avanzamos con la creación del archivo yaml para docker-compose con el fin de poder levantar a futuro la base Neo4j y la app en containers separados.

## **5. Entorno de desarrollo**
Para poder probar los cambios realizados en la aplicación a medida que los ibamos implementando, fue necesario montar el volumen local en el container de la app (originalmente realizabamos un COPY dentro del directorio del volumen al buildear el container) y setear flask en modo desarrollo para que escuche los cambios en los archivos en vivo.

## **6. Postman**
Una aplicación muy simple pero útil para crear y probar los request a la API del servicio. 

https://www.postman.com/downloads/

## **7. Estructura del proyecto y modularización de los servicios**
Siguiendo las buenas prácticas, la idea fue modularizar las diferentes partes definidas para el servicio:
- users
- products
- purchases
- recomendaciones

Para ello fue necesario explorar el framework de flask para entender cómo registrar las diferentes URLs a utilizar en cada uno de ellos mediante *blueprints*.

https://flask.palletsprojects.com/en/1.1.x/tutorial/views/

## **8. Mock de la base de datos**
Al comenzar a desarrollar los diferentes módulos fue útil comenzar con una forma de almacenamiento simple , por lo que la *base de datos* en esta primera instancia fue una lista precargada en memora mediante la cual se podría probar guardar y devolver los diferentes elementos a la vez que se daba forma a las entidades (en nuestro caso, usuario y productos *-que terminaron siendo únicamente libros para simplificar el caso de negocio*).

## **9. Neo4j**
Una vez armada la lógica principal y pensado el modelo de datos, fuimos en busca de una imagen de Neo4j para docker.

https://hub.docker.com/_/neo4j/

Y luego buscando algunos ejemplos encontramos cómo levantar Neo4j desde docker-compose, pasarle la info de autenticación mediante variables de entorno a la base y a la webapp y cómo conectar los servicios entre sí.

https://neo4j.com/labs/kafka/4.0/docker/

## **10. Driver de Neo4j**
Luego fuimos en busca de un driver de Neo4j para python. Nos inclinamos por usar el driver más básico para construir nosotros mismos las queries de ABM y así poder implementar los conceptos vistos en las clases del curso.

https://neo4j.com/developer/python/

Para utilizar el driver fue necesario comprender los conceptos de sesiones, transacciones y driver de la libreria de python utilizada.

https://neo4j.com/docs/api/python-driver/current/

Al implementar con el driver la conexión a la base de datos, tuvimos algunos inconvenientes con las conexiones abiertas y fue necesario implementar una lógica bastante común en el desarrollo de software que garantice que existe una única instancia de conexión a la base de datos a la vez y que al llamar a la clase siempre te devuelva la instancia existente en lugar de crear una nueva. Para ello implementamos una clase Singleton que resuelve estas cuestiones.

https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python

## **11. Constraints al inicio de la base**
Para agragar consistencia a la base de datos, se nos ocurrio correr un script de cypher que cree algunas constraints sobre la base, siempre y cuando éstas no existan.

Para esto fue necesario buildear la imagen de neo con el COPY del script a correr dentro del container y analizar las posibilidades para que corra automático al levantarse el container pero sin interferir con el inicio normal de la base.

Despues de dar vueltas en varios foros, encontramos esta solucion (con la que además tuvimos que entender un poco de bash y analizar el entrypoint de la imagen de Neo4j para docker):

https://stackoverflow.com/questions/48357238/how-can-i-run-cypher-scripts-on-startup-of-a-neo4j-docker-container
 
Para correr el script fue necesario crear variables de entorno con user y pass para pasar al cypher-shell.

https://neo4j.com/developer/kb/how-do-i-authenticate-with-cypher-shell-without-specifying-the-username-and-password-on-the-command-line/

## **12. Errores y status codes**
En esta instancia ya estabamos en condiciones de implementar un mejor manejo de errores y códigos de estado para contener internamente todos los imprevistos y mostrar mensajes de error consistentes.

https://flask.palletsprojects.com/en/1.1.x/errorhandling/#application-errors

https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

## **13. Testing**
Con las funcionalidades principales del servicio finalizadas, restaba repasar algunos conceptos generales de testing de aplicaciones:
- Unit test
- Integration test 
- E2E test

Para mejorar la comprension de estos temas tambien abordamos conceptos de funciones puras y no puras, side effects, dependencias, aislamiento de funcionalidades y mocks.  

Una vez comprendida la teoría, nos pusimos manos a la obra para implementar algunos test unitarios para nuestra app. Para ello optamos por las librerias pytest y pytest-mock.

https://pypi.org/project/pytest-mock/

Con el fin de no tener que levantar los containers una y otra vez al implementar nuevos test, y poder ir probandolos en un ambiente identico pero sin la instancia de base de datos (solo unit testing) encontramos el concepto de Multi-stage Dockerfile, mediante el cual un mismo dockerfile se puede desdoblar en la creacion de más de una imagen con características compartidas pero algunas diferencias. 

https://docs.docker.com/language/nodejs/run-tests/

De esta forma, cambiamos el dockerfile que buildea nuestra app para incorporarle una imagen para testing.

https://stackoverflow.com/questions/53093487/multi-stage-build-in-docker-compose

Finalemnte, para poder correr los test con la imagen preparada, creamos un pequeño archivo bash que hace el build de la imagen de test y levanta un container que la corre, ejecutando pytest (librería que levanta todos los archivos que encuentra con el formato test_*.py o *_test.py automaticamente).



