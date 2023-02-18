# Challenge Chileregistros

Proyecto django enfocado en el consumo de API y Web Scraping.

## Deploy

- Deploy AWS EC2: [Link](http://18.229.156.255/admin/) <br>
- Url de BikeSantiago: [Link](http://18.229.156.255/bikesantiago/networks/) <br>
- Url de seia: [Link](http://18.229.156.255/seia/seia_data/?limit=50)

# Índice
- [Challenge Chileregistros](#challenge-chileregistros)
  - [Deploy](#deploy)
- [Índice](#índice)
- [Descripción general](#descripción-general)
  - [log\_sys](#log_sys)
  - [seia](#seia)
  - [bikesantiago](#bikesantiago)
- [Instalación](#instalación)
  - [Linux](#linux)
  - [Windows:](#windows)
- [¿Como utilizarlo?](#como-utilizarlo)

# Descripción general

El proyecto cuenta con 3 apps principales:

## log_sys

App orientada al uso interno del proyecto, su principal objetivo es la de prestar servicio a las demás apps de manejo de errores y retorno de objeto de tipo Response para las consultas a los endpoints. Puede procesar cualquier clase de error y realizar las acciones correspondientes. Se puede actualizar de forma sencilla para el envío de errores 500 mediante mails en tiempo real. En carpeta apps/log_sys/logs se almacenan los logs de errores por app.

[Volver al Índice 🔝](#índice)
## seia

App enfocada en el Web scraping, en ella se aplica la librearía BS4 en conjunto de programación paralela, esta última para acortar el proceso principal el cual debe recorrer mas de 2800 vistas. En producción, por temas de limitaciones de capacidad de memoria y procesador de la máquina, se ajustaron los parámetros de workers al mínimo, por lo que el proceso de scraping tardaría mucho mas que en un computador con más capacidades. (Máquina virtual con 2 CPU 1 GB de memoria en total en plan gratuito).

[Volver al Índice 🔝](#índice)
## bikesantiago

App orientada al consumo de una API para extraer información y poblar la base de datos local. 
Su función principal posee tratamiento de varios casos en donde la data presentaba anormalidades, como, por ejemplo, la desaparición repentina de ciertas keys de diccionario, entre otros. Construye la data en orden para su coherencia y realiza comprobación de existencia de datos para realizar actualización o creación según corresponda. Se puede ejecutar sin perjudicar la data existente.

[Volver al Índice 🔝](#índice)
# Instalación

## Linux

1.	Instalar librerías necesarias para el proyecto:
    ```
    sudo apt-get update
    sudo apt-get install git python3.10 python3-pip virtualenv libpq-dev postgresql postgresql-contrib net-tools -y
    ```

2.	Crear base de datos en postgresql:
    ```
    sudo su postgres
    psql
    CREATE DATABASE nombre_bdd;
    CREATE USER nombre_usuario WITH PASSWORD 'password'; 
    ALTER USER nombre_usuario WITH PASSWORD 'password'; 
    ALTER ROLE nombre_usuario SET client_encoding TO 'utf8';
    ALTER ROLE nombre_usuario SET default_transaction_isolation TO 'read committed';
    ALTER ROLE nombre_usuario SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE nombre_bdd TO nombre_usuario;
    \q
    exit
    ```

3.	Clonar el repositorio:
    ```
    git clone https://github.com/GonzaloGSC/challenge_chileregistros.git
    cd path/to/challenge_chileregistros
    virtualenv env
    source env/bin/actívate
    pip install -r requirements_prod.txt
    ```

4. Archivo .env (enviado por mail):

    - Colocar .env en carpeta "backend" o core del proyecto.
    - Actualizar .env en carpeta "backend": STATIC_ROOT=/var/www/html
    - Editar .env añadiendo la public_ip en ALLOWED_HOSTS.
    - Actualizar las lineas:
        ```
        DATABASE_NAME=nombre_bdd
        DATABASE_USER=nombre_usuario
        DATABASE_PASSWORD=password
        DATABASE_HOST=localhost
        DATABASE_PORT=5432
        ```
5. Aplicar migraciones y crear superusuario:
    ```
    python manage.py migrate
    python manage.py createsuperuser
    ```
6. Correr proyecto:
    ```
    python manage.py runserver
    ```
[Volver al Índice 🔝](#índice)
## Windows:

1. Instalar Python 3.10: https://www.python.org/downloads/release/python-3100/

2. Instalar virtual env: 
    ```
    pip install virtualenv
    ```

3. Crear la base de datos en postgres con pgAdmin.

4.	Clonar el repositorio:
    ```
    git clone https://github.com/GonzaloGSC/challenge_chileregistros.git
    cd path/to/challenge_chileregistros
    virtualenv env
    source env/scripts/actívate
    pip install -r requirements.txt
    ```

5. Archivo .env (enviado por mail):

    - Colocar .env en carpeta "backend" o core del proyecto.
    - Actualizar .env en carpeta "backend": STATIC_ROOT=/var/www/html
    - Editar .env añadiendo la public_ip en ALLOWED_HOSTS.
    - Actualizar las lineas:
        ```
        DATABASE_NAME=nombre_bdd
        DATABASE_USER=nombre_usuario
        DATABASE_PASSWORD=password
        DATABASE_HOST=localhost
        DATABASE_PORT=5432
        ```

6. Aplicar migraciones y crear superusuario:
    ```
    python manage.py migrate
    python manage.py createsuperuser
    ```
7. Correr proyecto:
    ```
    python manage.py runserver
    ```
[Volver al Índice 🔝](#índice)

# ¿Como utilizarlo?

Debes ingresar a los links que se encuentran en la descripción general del proyecto, en ambos se admiten los metodos POST y GET. Si no se ven datos, debes realizar un POST primero. 

[Ir a Deploy 🔝](#deploy)