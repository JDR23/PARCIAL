Proyecto Tienda Online – FastAPI

Este proyecto implementa una tienda online como parte del Parcial #1 de la materia de Programación (prof. Alejandro Salgar). Está desarrollado en Python siguiendo principios de Programación Orientada a Objetos (POO) y expuesto como API REST con FastAPI.

Funcionalidades

Ver catálogo de productos

Agregar y remover productos del carrito

Ver resumen del carrito

Aplicar descuentos

Calcular subtotal, descuentos y total

Confirmar pago

Manejo de usuarios y facturación

Tecnologías

Python 3.x

FastAPI

Uvicorn

SQLite (archivo test.db)

PostgreSQL en la nube (Neon) con migraciones

Pydantic (validaciones)

Estructura del proyecto
├── crud/                # Operaciones CRUD (ej. crud_usuario.py)
├── entities/            # Entidades principales (Carrito, Cliente, Producto, Factura, Tipo_Producto)
├── models/              # Modelos de base de datos (Usuario, etc.)
├── routers/             # Definición de rutas/endpoints (usuario_router.py)
├── database.py          # Configuración de base de datos
├── db_conn.py           # Conexión a la base de datos
├── main.py              # Punto de entrada (inicia FastAPI)
├── schemas.py           # Esquemas de datos (Pydantic)
├── test.db              # Base de datos SQLite local
├── .env                 # Variables de entorno
└── README.md            # Documentación

Ejecución del proyecto

Clonar el repositorio:

git clone <URL_DEL_REPO>
cd <carpeta_del_proyecto>


Crear y activar entorno virtual:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Instalar dependencias:

pip install -r requirements.txt


Configurar variables de entorno en .env (ejemplo abajo).

Iniciar el servidor FastAPI:

uvicorn main:app --reload


Abrir en el navegador:

API: http://127.0.0.1:8000

Documentación Swagger: http://127.0.0.1:8000/docs

Documentación Redoc: http://127.0.0.1:8000/redoc

Ejemplo de .env
# Base de datos local (SQLite)
DATABASE_URL=sqlite:///./test.db

# Base de datos en Neon (PostgreSQL)
# Reemplaza <usuario>, <password>, <host> y <dbname> con tus credenciales de Neon
DATABASE_URL=postgresql://<usuario>:<password>@<host>/<dbname>


Ejemplo genérico con tu proyecto en Neon (tienda_online):

DATABASE_URL=postgresql://usuario:contraseña@ep-calm-meadow-39402852.us-east-2.aws.neon.tech/tienda_online


(nota: los datos de usuario y contraseña los genera Neon y deben pegarse aquí).

Migraciones con Alembic

El proyecto incluye integración con Alembic para manejar migraciones.

Generar nueva migración:

alembic revision --autogenerate -m "descripcion de la migracion"


Aplicar migraciones:

alembic upgrade head


Esto permite mantener sincronizado el esquema de la base de datos tanto en SQLite local como en Neon PostgreSQL remoto
