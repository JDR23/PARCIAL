"""
Script para crear el archivo .env con las credenciales de Neon
"""
import os

print("=" * 60)
print("CONFIGURACIÓN DE BASE DE DATOS NEON")
print("=" * 60)
print()

# Credenciales proporcionadas
PGUSER = "neondb_owner"
PGPASSWORD = "npg_cstL2xjMova6"

print(f"Usuario: {PGUSER}")
print(f"Contraseña: {'*' * len(PGPASSWORD)}")
print()

# Solicitar información faltante
print("Necesito la siguiente información de Neon:")
print()

# Host (endpoint)
host = input("Host (endpoint) de Neon (ej: ep-xxxxx.region.aws.neon.tech): ").strip()
if not host:
    print("Error: El host es requerido")
    exit(1)

# Nombre de la base de datos
database = input("Nombre de la base de datos (ej: neondb o tienda_online): ").strip()
if not database:
    database = "neondb"  # Valor por defecto
    print(f"Usando nombre por defecto: {database}")

# Construir la connection string
DATABASE_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@{host}/{database}?sslmode=require"

print()
print("=" * 60)
print("CONNECTION STRING GENERADA:")
print("=" * 60)
print(DATABASE_URL)
print()

# Confirmar creación del archivo .env
confirmar = input("¿Crear archivo .env con esta configuración? (s/n): ").strip().lower()

if confirmar == 's':
    # Crear el archivo .env
    env_content = f"""# Configuración de Base de Datos Neon PostgreSQL
DATABASE_URL={DATABASE_URL}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print()
    print("✅ Archivo .env creado exitosamente!")
    print()
    print("Próximos pasos:")
    print("1. Reinicia el servidor: uvicorn main:app --reload")
    print("2. Verifica que veas: [INFO] Usando base de datos: ...")
    print()
else:
    print()
    print("No se creó el archivo .env")
    print("Puedes crear el archivo manualmente con:")
    print(f"DATABASE_URL={DATABASE_URL}")

