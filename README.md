# **Tópicos Especiales en Telemática: Reto 1**

## Descripción del proyecto

Este repositorio es la solución al reto planteado para el curso de Tópicos Especiales en Telemática de la Universidad EAFIT (Semestre 2021-2).

En este archivo se detallará información del reto solucionado, el contenido del proyecto, la infraestructura desplegada y los servicios utilizados.

## Problema: Base de datos distribuida

Tenemos un conjunto de NODOS, los cuales almacenarán registros de una aplicación cliente en el formato <k,v> (key, value). El objetivo es diseñar e implementar un sistema ‘minimalista’ que permita almacenar datos distribuidos en los NODOS por parte de los clientes. Por <i>minimalista</i> quiere decir que usará una visión desde la más simple, pero deberá dejar explicito los retos reales que enfrentan sistemas similares <i>robustos</i>, escalables, confiables, consistentes. Realice todos los supuestos y restricciones que considere.

A continuación se enumeran los retos principales del sistema:

- Almacenamiento distribuido de datos y Recuperación Distribuida o Centralizada.
- Replicación
- Particionamiento
- Tolerancia a fallos
- Escalabilidad
- WORM vs WMRM
- Cliente/Servidor vs P2P vs hibrido C/S-P2P, con todas las variantes posibles de C/S y P2P.
- Transacciones, Bloque u Objetos.

Requerimientos:
- La visión global del sistema es un cliente externo interesado en Almacenar datos <k,v> en un sistema distribuido.
- El sistema permitirá almacenar n registros con la misma clave <k>
- La recuperación de los datos se realizará por <k>
- Escenarios para k retornando un solo valor, k retornando algunos datos, k retornando muchos datos, k retornando gran cantidad de datos.
- Puede ser diseñado como una base de datos distribuida <k,v> o como un sistema de archivos distribuido, o como un sistema de mensajería distribuido.
- Idear, diseñar e implementar una aplicación ejemplo –separada del sistema de almacenamiento distribuido – que    pruebe la funcionalidad del Sistema de Almacenamiento y Recuperación Distribuido.
- Lo puede implementar sobre protocolos TCP/UDP con sockets o con protocolos HT.

## Solución del problema

Para resolver esto, tomamos el caso de una base de datos distribuida, y empezamos a discutir sobre cuál sería la mejor manera de implementarlo. Empezaremos mostrando nuestra solución final de infraestructura.

[IMAGEN]

Hay tres operaciones elementales por definir en este problema UPLOAD (cargar archivos), READ (leer archivos) y DELETE (eliminar archivos). Explicaremos, a continuación, la participación de los diferentes actores de esta infraestructura (las máquinas instanciadas) en las distintas operaciones.

## Cliente

## Servidor MOISES

## Servidor HERMES



## Participantes

- <a href="https://github.com/dcalleg707"><img src="https://image.flaticon.com/icons/png/512/25/25231.png" width=20></a> David Calle González

- <a href="https://github.com/juansedo"><img src="https://image.flaticon.com/icons/png/512/25/25231.png" width=20></a> Juan Sebastián Díaz Osorio 

- <a href="https://github.com/sanhidalgoo"><img src="https://image.flaticon.com/icons/png/512/25/25231.png" width=20></a> Santiago Hidalgo Ocampo 
