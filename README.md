

# CAUS - Certificates generator

Generador de certificados para los asistentes a las actividades del Club de Algoritmia de la Universidad de Sevilla.


## Instalación

 1. Descarga el repositorio. Puedes hacerlo como zip desde [la  página de GitHub](https://github.com/algoritmiaUS/certificates-generator) o directamente utilizando Git: `git clone git@github.com:algoritmiaUS/certificates-generator.git`.

 2. Antes de empezar tienes que instalar [resvg](https://github.com/linebender/resvg/releases) en tu sistema. Se trata de una librería desarrollada en Rust que permite convertir imágenes SVG en archivos PNG.

    Nota: Si tu ordenador está poseído por Windows necesitarás descargar el archivo .exe correspondiente y asegurarte de guardarlo en un directorio que aparezca en la variable PATH.

 3. Instala [Python 3](https://www.python.org/downloads/) (si es que no lo tienes ya). Este código ha sido probado para Python 3.12.1 y no requiere más dependencias externas.


# Utilización

 1. Indica los nombres de los participantes en el archivo CSV "./data/participants.csv", creándolo si no existe. El archivo debe incluir una línea de cabeceras.
 2. Indica los nombres de los ganadores en el archivo CSV "./data/winners.csv", creándolo si no existe. El archivo debe incluir una línea de cabeceras.
 3. Por último, introduce el siguiente comando en la terminal: `python ./create_certificates.py`.
 4. Ya tienes los resultados en el directorio "./out"!
