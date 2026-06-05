# Introducción

En este documento se presenta la especificación del desarrollo de la base de datos para **CampusBike**, una empresa dedicada a la comercialización de bicicletas, repuestos y accesorios. La organización ha identificado la necesidad de implementar un sistema eficiente y centralizado que permita organizar, analizar y gestionar la información del negocio de manera adecuada. Entre las principales problemáticas detectadas se encuentran la gestión deficiente de clientes y repuestos, la ineficiencia en la cadena de suministro y las dificultades para analizar las ventas y compras realizadas.

A lo largo de este documento se describe de manera estructurada el proceso de diseño de una base de datos capaz de solucionar los problemas mencionados, permitiendo una gestión eficiente de la información, así como un almacenamiento y manipulación de datos confiables y accesibles para la empresa. Para ello, se desarrollaron los modelos fundamentales de una base de datos: el modelo conceptual, el modelo lógico y el modelo físico.

El modelo conceptual constituye una representación general de los requerimientos del sistema, identificando las principales entidades, atributos y relaciones involucradas. Su propósito es proporcionar una visión global del funcionamiento de la base de datos antes de abordar aspectos técnicos específicos.

Posteriormente, el modelo lógico toma como base el modelo conceptual y define una estructura más detallada de los datos, estableciendo tablas, atributos, llaves primarias, llaves foráneas y cardinalidades. Además, en esta etapa se realiza el proceso de normalización con el fin de garantizar la integridad y consistencia de la información.

Finalmente, el modelo físico representa la implementación de la base de datos en un sistema gestor, considerando aspectos relacionados con los tipos de datos, restricciones y demás elementos necesarios para su funcionamiento.

La elaboración de estos modelos tiene como objetivo proporcionar una representación clara y organizada de los sistemas de recopilación, almacenamiento y administración de información de CampusBike, facilitando su comprensión por parte de analistas, diseñadores e ingenieros encargados del desarrollo e implementación de la solución.

# Caso de Estudio

En el competitivo sector de la comercialización de bicicletas, CampusBike enfrenta diversos desafíos relacionados con la gestión de la información. La ausencia de un sistema centralizado para organizar, analizar y utilizar los datos afecta directamente la eficiencia operativa y la capacidad de toma de decisiones de la empresa.

Entre los problemas más relevantes se encuentran:

## 1. Gestión Deficiente de Clientes

La falta de un sistema estructurado dificulta el seguimiento de las interacciones con los clientes, limitando la posibilidad de ofrecer servicios personalizados y estrategias efectivas de fidelización.

## 2. Ineficiencia en la Cadena de Suministro

La administración de proveedores, inventarios y pedidos mediante procesos manuales o sistemas dispersos genera errores, retrasos y dificultades para mantener la disponibilidad de productos de acuerdo con la demanda.

## 3. Dificultades en el Análisis de Ventas y Compras

La ausencia de una base de datos robusta impide realizar análisis precisos sobre el comportamiento de las ventas y las compras, limitando la generación de reportes y la toma de decisiones estratégicas basadas en datos confiables.

## 4. Gestión Ineficiente de Repuestos

La falta de control sobre los repuestos y accesorios ocasiona problemas de inventario, tales como exceso de existencias o desabastecimiento, afectando la calidad del servicio y la satisfacción de los clientes.

## Solución Propuesta

Para abordar estas necesidades, CampusBike requiere el diseño e implementación de una base de datos robusta y funcional que permita gestionar de manera eficiente la información relacionada con sus operaciones comerciales.

La solución debe incluir los siguientes componentes:

### Gestión de Clientes

Registro detallado de la información de los clientes, incluyendo datos personales, historial de compras e interacciones, con el fin de ofrecer una atención más personalizada y eficiente.

### Gestión de Proveedores

Centralización de la información de los proveedores, condiciones de suministro y seguimiento de pedidos, optimizando la administración de la cadena de abastecimiento.

### Gestión de Ventas y Compras

Registro y análisis detallado de las operaciones de venta y compra para facilitar la generación de reportes y la toma de decisiones estratégicas.

### Gestión de Inventarios y Repuestos

Control preciso del inventario de bicicletas, repuestos y accesorios, garantizando la disponibilidad de productos y reduciendo los costos asociados al exceso o la escasez de existencias.

Con base en estos requerimientos y en la solución propuesta, se desarrollará una base de datos que contemple todos los elementos necesarios para garantizar una gestión eficiente, segura y organizada de la información de CampusBike.

# Planificación

## Construcción del Modelo Conceptual

El modelo conceptual representa de forma gráfica y estructurada la información que gestiona el sistema de CampusBike, sin incluir detalles técnicos relacionados con la implementación, como llaves primarias, llaves foráneas o tipos de datos.

Durante su construcción se analizó el contexto empresarial, identificando los procesos fundamentales de la organización, los requerimientos de los usuarios y las reglas de negocio que deben ser consideradas dentro del sistema.

Este modelo permite establecer una comunicación clara entre las necesidades de la empresa y el diseño posterior de la base de datos, garantizando una transición adecuada hacia las etapas más técnicas del desarrollo.

### Descripción

El modelo conceptual se elaboró utilizando la metodología Entidad-Relación (E-R), donde las entidades representan los objetos principales del sistema, como clientes, productos, proveedores, ventas o compras. Los atributos corresponden a las características que describen dichas entidades, mientras que las relaciones representan los vínculos existentes entre ellas, definidos mediante cardinalidades que indican la forma en que interactúan dentro del sistema.
