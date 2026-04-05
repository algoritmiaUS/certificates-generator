

# CAUS - Certificates generator

Generador de certificados para los asistentes a las actividades del Club de Algoritmia de la Universidad de Sevilla.


## Instalación

 1. Descarga el repositorio. Puedes hacerlo como zip desde [la página de GitHub](https://github.com/algoritmiaUS/certificates-generator) o directamente utilizando Git: `git clone git@github.com:algoritmiaUS/certificates-generator.git`.

 2. Antes de empezar tienes que instalar [resvg](https://github.com/linebender/resvg/releases) en tu sistema. Se trata de una librería desarrollada en Rust que permite convertir imágenes SVG en archivos PNG.

> [!NOTE]
> Si tu ordenador está poseído por Windows necesitarás descargar el archivo .exe correspondiente y asegurarte de guardarlo en un directorio que aparezca en la variable PATH.

 3. Instala [Python 3](https://www.python.org/downloads/) (si es que no lo tienes ya). Este código ha sido probado para Python 3.12.1.

 4. Instala las dependencias de Python: `pip install -r requirements.txt`.


## Configuración

1. Crea un archivo llamado `.env` en la raíz del proyecto para definir la configuración. Puedes utilizar el archivo [.env.sample](./.env.sample) como referencia.
2. Preparación del archivo CSV. Ambos scripts de este proyecto (el generador y el que envía los correos) leen de un **único archivo CSV** (por defecto `participants.csv`), que debe incluir una línea de cabeceras con los siguientes campos:
    - `position`: Indica si la persona ha ganado. Usa `1`, `2` o `3` para las medallas de oro, plata o bronce. Deja este campo vacío o usa `0` para participantes regulares.
    - `name`: Nombre del destinatario que aparecerá en el certificado.
    - `email`: Correo al que se le enviará el resultado.


## Generación de certificados

 1. Rellena el archivo configurado en tu `.env` con los datos de los participantes (como se indica arriba).
 2. Introduce el siguiente comando en la terminal: `python ./create_certificates.py`.
 3. Ya tienes los resultados en el directorio indicado (por defecto `./out/`)!

Para ver otras opciones ejecuta `python ./create_certificates.py --help`.


## Envío de emails


### Configuración de la API de Gmail

 1. Ve a [Google Cloud Console](https://console.cloud.google.com/) y crea un nuevo proyecto (o usa uno existente).
 2. Habilita la **Gmail API** en *APIs & Services > Library*.
 3. Ve a *APIs & Services > Credentials* y crea unas credenciales de tipo **OAuth 2.0 Client ID** (Application type: Desktop app).
 4. Descarga el archivo JSON resultante y guárdalo en la raíz del repositorio como `auth.json`.
 5. La primera vez que ejecutes el script se abrirá el navegador para que autorices el acceso a la cuenta de Gmail. Se generará automáticamente un archivo `token_gmail_v1.pickle` con las credenciales ya autorizadas.


### Configuración y ejecución

 1. Asegúrate de tener el archivo `.env` completo y tu archivo CSV listo.
 2. Opcional: Modifica cualquier texto de los correos (`SUBJECT`, `MESSAGE`) si necesitas cambiarlos para diferentes envíos.
 3. Ejecuta `python ./send_emails.py`.


## Licencia

Al realizar contribuciones a este proyecto, aceptas automáticamente que tu código se publique bajo los términos de la [Licencia MIT](LICENSE.txt).
