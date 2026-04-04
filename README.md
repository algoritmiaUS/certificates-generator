# CAUS - Certificates generator

Generador de certificados para los asistentes a las actividades del Club de Algoritmia de la Universidad de Sevilla.

## Instalación

 1. Descarga el repositorio. Puedes hacerlo como zip desde [la página de GitHub](https://github.com/algoritmiaUS/certificates-generator) o directamente utilizando Git: `git clone git@github.com:algoritmiaUS/certificates-generator.git`.

 2. Antes de empezar tienes que instalar [resvg](https://github.com/linebender/resvg/releases) en tu sistema. Se trata de una librería desarrollada en Rust que permite convertir imágenes SVG en archivos PNG.

> [!NOTE]
> Si tu ordenador está poseído por Windows necesitarás descargar el archivo .exe correspondiente y asegurarte de guardarlo en un directorio que aparezca en la variable PATH.

 3. Instala [Python 3](https://www.python.org/downloads/) (si es que no lo tienes ya). Este código ha sido probado para Python 3.12.1.

 4. Instala las dependencias de Python: `pip install -r requirements.txt`.

## Generación de certificados

 1. Indica los nombres de los participantes en el archivo CSV "./data/participants.csv", creándolo si no existe. El archivo debe incluir una línea de cabeceras.
 2. Indica los nombres de los ganadores en el archivo CSV "./data/winners.csv", creándolo si no existe. El archivo debe incluir una línea de cabeceras.
 3. Por último, introduce el siguiente comando en la terminal: `python ./create_certificates.py`.
 4. Ya tienes los resultados en el directorio "./out"!

Para ver otras opciones ejecuta `python ./create_certificates.py --help`.

## Envío de emails

### Configuración de la API de Gmail

 1. Ve a [Google Cloud Console](https://console.cloud.google.com/) y crea un nuevo proyecto (o usa uno existente).
 2. Habilita la **Gmail API** en *APIs & Services > Library*.
 3. Ve a *APIs & Services > Credentials* y crea unas credenciales de tipo **OAuth 2.0 Client ID** (Application type: Desktop app).
 4. Descarga el archivo JSON resultante y guárdalo en la raíz del repositorio como `auth.json`.
 5. La primera vez que ejecutes el script se abrirá el navegador para que autorices el acceso a la cuenta de Gmail. Se generará automáticamente un archivo `token_gmail_v1.pickle` con las credenciales ya autorizadas.

### Preparación del archivo de mailing

El archivo de mailing (CSV o Excel) debe contener los datos de los participantes para el envío. Es **muy importante** que los nombres en este archivo sean exactamente los mismos que se usaron en los archivos CSV al generar los certificados (`participants.csv` o `winners.csv`), ya que se usan para buscar el PDF correspondiente de cada persona.

Ten en cuenta que, dependiendo de la estructura de tu archivo de mailing, puede que necesites editar la función `process_mailing_list` dentro de `send_emails.py` para indicar qué columnas deben ser leídas (por defecto el script toma la primera columna como el nombre y la segunda como el email).

### Configuración y ejecución

 1. Abre `send_emails.py` y edita las constantes de la sección `# Personalize`:
    - `EMAIL`: dirección de correo desde la que se envían los emails.
    - `SUBJECT`: asunto del email.
    - `MESSAGE`: cuerpo del email.
    - `MAILING_LIST_FILE`: ruta al archivo CSV o Excel con los datos.
 2. Ejecuta `python ./send_emails.py`.

## Licencia

Al realizar contribuciones a este proyecto, aceptas automáticamente que tu código se publique bajo los términos de la [Licencia MIT](LICENSE.txt).
