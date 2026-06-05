# PIZZERÍA

## Introducción

En este documento se halla la especificación del desarrollo de la base de datos realizada para una pizzería que se encuentra con la necesidad de crear un sistema eficiente y centralizado para organizar, analizar y utilizar los datos del negocio. Entre los problemas más destacados se encuentran la gestión deficiente de clientes y productos, la ineficiencia en la cadena de suministro y las dificultades en el análisis de ventas y compras.

Aquí se muestra de forma esquematizada la creación de una base de datos que solucione los problemas previamente mencionados para lograr una gestión eficiente de la información, el almacenamiento y la manipulación de datos de manera accesible para la empresa. Para lograr esto se realizaron los modelos necesarios para la base de datos: conceptual, lógico y físico.

El modelo conceptual es una descripción general de los requerimientos, identificando las principales entidades, atributos y relaciones de los datos para crear una representación general del sistema.

El modelo lógico trabaja sobre lo desarrollado en el modelo conceptual, implementando una estructura más específica de los datos, definiendo tablas, llaves primarias, llaves foráneas y cardinalidades. Una vez logrado este modelo, se realiza el proceso de normalización hasta sus tres formas normales.

Finalmente, el modelo físico permite la implementación de la base de datos, teniendo en cuenta aspectos relacionados con el lenguaje de definición de datos y los tipos de datos utilizados.

La representación de estos modelos tiene como objetivo facilitar la comprensión de los sistemas de recopilación y administración de información, ayudando a analistas e ingenieros a interpretar de manera efectiva los datos.

---

# Caso de Estudio

El propósito de este proyecto es diseñar una base de datos que permita gestionar eficientemente los productos, combos, pedidos y clientes de una pizzería. El sistema debe almacenar información sobre pizzas, panzarottis, bebidas, postres, adiciones y el menú disponible.

Además, se deberán registrar los pedidos de los clientes, que pueden ser para consumir en el establecimiento o para recoger.

## Problema

La pizzería actualmente no cuenta con un sistema centralizado para gestionar sus productos y pedidos, lo que genera confusión al manejar inventarios, combos y opciones de pedidos. También resulta difícil realizar seguimiento a los productos más vendidos o personalizar pedidos.

Por lo tanto, se requiere un sistema que permita gestionar de manera eficiente el menú, las combinaciones de productos, las ventas y los pedidos.

## Características Principales

*(Agregar aquí la lista de características principales del sistema.)*

---

# Planificación

## Construcción del Modelo Conceptual

Este modelo plasma gráficamente de forma general y estructurada la información que gestiona el sistema de la pizzería, sin especificaciones técnicas como el uso de llaves primarias o detalles de implementación.

Durante la creación de este modelo se analizó el contexto especificado por la empresa, enfocándose en los detalles clave del funcionamiento de la tienda, los requerimientos de los usuarios y demás aspectos importantes.

Este modelo permite una comunicación efectiva entre las reglas del negocio y el sistema físico de gestión de bases de datos, garantizando una transición adecuada hacia etapas más técnicas del diseño.

### Descripción

Este modelo se realizó utilizando el enfoque Entidad-Relación (E-R), donde una entidad representa un objeto del sistema, como un cliente, pedido o producto. Los atributos son las propiedades que describen dichas entidades y las relaciones representan los vínculos existentes entre ellas mediante cardinalidades.

---

## Construcción del Modelo Lógico

Este modelo brinda mayor nivel de detalle que el modelo conceptual, agregando atributos, tipos de datos y requisitos para la información, incluyendo llaves primarias, llaves foráneas y restricciones definidas en las especificaciones.

Durante la construcción del modelo lógico se añaden los detalles necesarios para representar adecuadamente en una base de datos las ideas generales descritas en el modelo conceptual.

### Descripción

En el modelo lógico, las entidades se transforman en tablas. Las columnas representan los atributos y se incluyen elementos importantes como:

* Llaves primarias (PK).
* Llaves foráneas (FK).
* Cardinalidades.
* Tipos de datos.
* Longitudes de los campos.

### Gráfica

*(Insertar aquí la gráfica del modelo lógico.)*

### Descripción Técnica

Cada tabla corresponde a una entidad identificada en el modelo conceptual.

Los atributos cuentan con:

* Tipo de dato.
* Longitud.
* Restricciones.

Además, se definen las llaves primarias (PK) para identificar de forma única cada registro y las llaves foráneas (FK) para establecer relaciones entre tablas.

Todas las tablas cuentan con un identificador único denominado `id_nombre_entidad`, de tipo `INTEGER`.

Los campos como nombres, direcciones y teléfonos utilizan el tipo `VARCHAR` con longitud específica para optimizar almacenamiento y rendimiento.

Las fechas se almacenan utilizando el tipo `DATE` o `DATETIME`.

Los valores monetarios se representan mediante el tipo `DECIMAL`.

La cardinalidad utilizada corresponde a la representación estándar de diagramas ERD, manteniendo las relaciones definidas en el modelo conceptual.

---

## Construcción del Modelo Físico

Este modelo representa la implementación específica de la base de datos, incluyendo tablas, columnas y demás objetos físicos necesarios.

### Descripción

Con base en el análisis lógico y las restricciones definidas previamente, se especifica la estructura de las tablas para su implementación en MySQL.

### Código

```sql
USE pizzeria;

CREATE TABLE consumir_fuera (
    id_consumir_fuera INT PRIMARY KEY AUTO_INCREMENT,
    hora_pedido DATETIME
);

CREATE TABLE consumir_tienda (
    id_consumir_tienda INT PRIMARY KEY AUTO_INCREMENT,
    mesa INT
);

CREATE TABLE Cliente (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(25),
    direccion VARCHAR(25),
    numero_telefono INT
);

CREATE TABLE Pedidos (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    consumir_fuera INT,
    consumir_tienda INT,
    fecha DATETIME,
    valor DECIMAL(10,3),
    cliente INT,
    FOREIGN KEY (consumir_fuera)
        REFERENCES consumir_fuera(id_consumir_fuera),
    FOREIGN KEY (consumir_tienda)
        REFERENCES consumir_tienda(id_consumir_tienda),
    FOREIGN KEY (cliente)
        REFERENCES Cliente(id_cliente)
);

CREATE TABLE Administrador (
    id_administrador INT PRIMARY KEY
);

CREATE TABLE Inventario (
    id_inventario INT PRIMARY KEY,
    tienda INT,
    productos VARCHAR(25)
);

CREATE TABLE Tienda (
    id_tienda INT PRIMARY KEY,
    id_administrador INT,
    inventario INT,
    pedido INT,
    FOREIGN KEY (inventario)
        REFERENCES Inventario(id_inventario),
    FOREIGN KEY (pedido)
        REFERENCES Pedidos(id_pedido)
);

CREATE TABLE Pedido_personalizado (
    id_pedido_personalizado INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT,
    FOREIGN KEY (id_pedido)
        REFERENCES Pedidos(id_pedido)
);

CREATE TABLE Combo (
    id_combos INT PRIMARY KEY AUTO_INCREMENT,
    combo1 INT,
    combo2 INT
);

CREATE TABLE Productos (
    id_menu INT PRIMARY KEY AUTO_INCREMENT,
    pizzas VARCHAR(30),
    panzerottis VARCHAR(30),
    bebidas VARCHAR(30),
    postres VARCHAR(30),
    combo INT,
    FOREIGN KEY (combo)
        REFERENCES Combo(id_combos)
);

CREATE TABLE Ingredientes (
    id_ingredientes INT PRIMARY KEY AUTO_INCREMENT,
    masa VARCHAR(30),
    aceite VARCHAR(30),
    vegetales VARCHAR(30),
    quesos VARCHAR(30),
    condimentos VARCHAR(30),
    salsas VARCHAR(30),
    carnes VARCHAR(30),
    producto INT,
    FOREIGN KEY (producto)
        REFERENCES Productos(id_menu)
);

CREATE TABLE Adicionales (
    id_adicional INT PRIMARY KEY AUTO_INCREMENT,
    pizza_extra_queso INT,
    panzerotti_extra_queso INT
);
```

### Descripción Técnica

El sistema gestor de bases de datos utilizado es MySQL.

La sintaxis general utilizada para crear tablas es:

```sql
CREATE TABLE nombre_tabla (
    nombre_columna tipo_dato parametros
);
```

Esta estructura permite definir entidades, atributos, tipos de datos, llaves primarias, llaves foráneas y demás restricciones necesarias para la correcta gestión de la información.

---

# Diagrama E-R

Para el desarrollo de este diagrama se utilizó el modelo Entidad-Relación, donde las entidades representan objetos del sistema, los atributos describen sus características y las relaciones establecen los vínculos existentes entre ellas.

## Descripción

A partir de los modelos desarrollados anteriormente, la estructura esquematizada se traduce al código SQL utilizado en MySQL, permitiendo implementar todas las entidades, atributos, llaves, cardinalidades y relaciones definidas durante el diseño.

## Descripción Técnica

La creación de las tablas dentro del SGBD se realiza mediante el comando:

```sql
CREATE TABLE
```

Por ejemplo, para la tabla de órdenes se define previamente la entidad identificada durante el modelado.

Cada columna posee:

* Nombre.
* Tipo de dato.
* Restricciones.

Por ejemplo:

* `id_orden` → Llave primaria (PK).
* Tipo de dato → `INT`.

Estas características permiten identificar de forma única cada registro dentro de la tabla.







# Caso de Estudio
El propósito de este examen es diseñar una base de datos que permita gestionar eficientemente los productos, combos, pedidos y clientes de una pizzería. El sistema debe almacenar información sobre pizzas, panzarottis, otros productos no elaborados (bebidas, postres, etc.), adiciones y el menú disponible. Además, se deberán registrar los pedidos de los clientes, que pueden ser para consumir en el lugar o para recoger.
Problema

La pizzería actualmente no tiene un sistema centralizado para gestionar sus productos y pedidos, lo que genera confusión al manejar inventarios, combos y opciones de pedidos. También resulta difícil hacer un seguimiento de los productos más vendidos o personalizar pedidos. Por lo tanto, se requiere un sistema que permita gestionar de manera eficiente el menú, las combinaciones de productos, las ventas, y los pedidos.
Características Principales





























Planificación

Construcción del Modelo Conceptual
Este modelo plasma gráficamente de forma general y estructurada la información que gestiona el sistema de Pizzerias, sin especificaciones en aspectos técnicos como el uso de llaves primarias o de implementación. 
En la creación de este modelo, se analizó el contexto especificado por la empresa, enfocándose en los detalles claves del funcionamiento de la tienda, los requerimientos de los usuarios y demás requerimientos importantes. Este modelo permite una comunicación segura entre las reglas empresariales y el sistema físico de gestión de bases de datos, garantizando una transición efectiva hacia etapas más técnicas del diseño.
Descripción
Este modelo se realizó en base a entidad-relación, en la que una entidad es un objeto ya sea un cliente, pedido o producto que previamente es gestionado en la base de datos. Los atributos son las propiedades que describen y se relacionan con estas entidades. Las relaciones describen los vínculos entre entidades definiendo la interacción que se representa por las cardinalidades.

Construcción del Modelo Lógico
Este modelo busca brindar más contexto del que el modelo conceptual específico como se evidenció con anterioridad agregando atributos, asignando tipos de datos y especificando requisitos para la información incluyendo las llaves principales y restricciones dadas en las especificaciones.
Durante la construcción del modelo lógico, se añaden detalles para documentar completamente cómo se representarán en una base de datos las ideas generales descritas en el modelo conceptual.

Descripción
La forma en que se representan los datos en este modelo varía en comparación con el conceptual. En el modelo lógico las tablas, son las entidades, esto no significa que sean las mismas, ya que cada tabla tiene su respectiva entidad, entidades son las filas. Las columnas son los atributos de esa tabla y otros elementos importantes como las llaves primarias representadas por PK, llave foránea representada por FK, la cardinalidad y  la especificación del tipo de datos junto la cantidad de estos.
Gráfica


Descripción Técnica
Cada tabla corresponde a una entidad identificada en el modelo conceptual por un rectángulo, ahora transformada en una representación más detallada por los atributos antes eclipses, cada uno de estos atributos cuenta con tipo y longitud, asimismo se definen las llaves primarias PK para identificar de forma única cada registro dentro de sus respectivas tablas, así como claves foráneas FK que permiten establecer relaciones entre ellas, asegurando de dependencia de datos.

En las tablas todas cuentan con un atributo que tiene un llave primaria, nombrada id junto al nombre de la entidad y el tipo de INTEGER de longitud no especificada, es decir, ( ). Para los datos como nombre, apellido, direcciones y teléfono son datos tipo VARCHAR con longitud especificada para mejorar y asegurar el rendimiento y almacenamiento. Las fechas son datos tipo DATE. 
Los precios unitarios y totales son representados en tipo DECIMAL con longitud de (3,1) el primer dígito indica el entero y el otro los decimales.

La cardinalidad que se usó es de ERD, se mantiene la misma del modelo conceptual pero traducida a este tipo de cardinalidad.
Construcción del Modelo Físico
Este modelo permite la representación mucho más específica que tiene en cuenta todos los detalles de los elementos de datos en una base de datos junto a las tablas, columnas y otros objetos físicos utilizados para implementar los conceptos trabajados y mencionados para la base de datos de la Pizzeria.
Descripción
Con el respectivo análisis de la lógica y restricciones de lo que se va realizar especificando la estructura de las tablas. La herramienta a usar en esta base de datos es MYSQL, ya con los modelos anteriormente realizados junto la complementación de la normalización, la creación del código es seguir la misma estructura.
Código
use pizzeria;
create table consumir_fuera (
id_consumir_fuera int primary key auto_increment,
hora_pedido datetime
);
create table consumir_tienda (
id_consumir_tienda int primary key auto_increment,
mesa int
);
CREATE TABLE Cliente (
 id_cliente INT PRIMARY KEY AUTO_INCREMENT,
 nombre VARCHAR(25),
 direccion VARCHAR(25),
 numero_telefono INT
);
CREATE TABLE Pedidos (
 id_pedido INT PRIMARY KEY AUTO_INCREMENT,
 consumir_fuera int,
 consumir_tienda INT,
 fecha datetime,
 valor decimal(10,3),
 cliente int,
 FOREIGN KEY (consumir_fuera) REFERENCES consumir_fuera(id_consumir_fuera),
 FOREIGN KEY (consumir_tienda) REFERENCES consumir_tienda(id_consumir_tienda), 
 FOREIGN KEY (cliente) REFERENCES Cliente (id_cliente)
);
create table Administrador (
id_administrador int primary key);
create table Inventario(
id_inventario int primary key,
tienda int,
productos varchar (25) );
create table Tienda (
id_tienda int primary key,
id_administrador int,
inventario int,
pedido int,
FOREIGN KEY (id_administrador) REFERENCES Administrador (id_cliente),
FOREIGN KEY (inventario) REFERENCES Inventario (id_inventario),
FOREIGN KEY (pedido) REFERENCES Pedidos (id_pedido));
create table Pedido_personalizado (
id_pedido_personalizado INT PRIMARY KEY AUTO_INCREMENT,
id_pedido int,
FOREIGN KEY (id_pedido) REFERENCES Pedidos (id_pedido)
);
create table Combo(
id_combos int PRIMARY KEY AUTO_INCREMENT,
combo1 int,
combo2 int
);
create table Productos (
id_menu int PRIMARY KEY AUTO_INCREMENT,
pizzas varchar (30),
panzerottis varchar(30),
bebidas varchar(30),
postres varchar(30),
combo int,
FOREIGN KEY (combo) REFERENCES Combo (id_combos));
create table Ingredientes(
id_ingredientes int PRIMARY KEY AUTO_INCREMENT,
masa varchar (30),
aceite varchar(30),
vegetales varchar(30),
quesos varchar(30),
condimentos varchar(30),
salsas varchar(30),
carnes varchar(30),
producto int(),
FOREIGN KEY (producto) REFERENCES Productos (id_menu));
create table Adicionales (
id_adicional int PRIMARY KEY AUTO_INCREMENT,
pizza_extra_queso int,
panzerotti_exta_queso int
);
select * from Productos;
show tables;
INSERT INTO Cliente (nombre, direccion, numero_telefono)VALUES ('Adriana', 'Carrera 22', 906788888),('Pedro', 'Carrera 20', 70679888),('Juan', 'Carrera 2', 7806788), ('Carmen', 'Calle 40', 70699788), ('Sofia', 'Calle 45', 8969568);
INSERT INTO Administrador (id_administrador) VALUES ('1');
INSERT INTO Inventario (id_inventario, tienda, productos) values (6, 10, 'vegetales'), (7, 3, 'salsas'), (3, 2, 'masas'), (4, 1, 'condimentos');
INSERT INTO Ingredientes (masa, aceite, vegetales, quesos, condimentos, salsas, carnes, producto) values ('madre', 'oliva', 'tomate', 'doble_crema', 'condimentos', 'salsas', 'carnes', 1);
insert into Productos (pizzas, panzerottis, bebidas, postres, combo) values ('peperonni', 'camaron', 'gaseosa', 'limon', 0)

Descripción Técnica
El sistema gestor de base de datos en este caso es MYSQL, se sigue la estructura de:
CREATE TABLE Nombre_tabla, (Nombre_columna  tipo de dato  parametro1  parametro2).
Esto se hace para definir las tablas con sus entidades y atributos con sus respectivas especificaciones como tipo, llaves primarias o foráneas y longitud en el sistema gestor que posteriormente mostrará las tablas con un correcto gestionamiento.
Diagrama E-R
Para el desarrollo de este diagrama, como se mencionó con anterioridad en el modelo conceptual, el modelo consiste sobre una entidad que es un objeto ya sea un cliente, pedido o producto que previamente es gestionado en la base de datos. Los atributos son las propiedades que describen y se relacionan con estas entidades. Las relaciones describen los vínculos entre entidades definiendo la interacción que se representa por las cardinalidades manejadas.
Descripción
Al tener con claridad los modelos anteriores, al pasar la estructura esquematizada en los diagramas a el código basado en MYSQL con la estructura trabajada en el modelo físico para este sistema gestor de datos, este mismo realiza todo el trabajo concretado con sus características, atributos, llaves y respectivas cardinalidades y relaciones.

Descripción Técnica



Para la creación de las tablas en el SGBD es por medio del el comando CREATE TABLE, en este ejemplo la tabla a realizar es la de Ordenes por lo que se escribe el comando y nombre de esta, identificada anteriormente como una entidad.

 Una columna tiene un nombre y un tipo de datos como es mostrado en el modelo lógico. Nombre id_orden que es una llave primario identificada como PK y su tipo que es entero.


