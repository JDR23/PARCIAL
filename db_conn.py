import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    record = cur.fetchone()
    print(" Conectado a:", record)
    cur.close()
    conn.close()
except Exception as e:
    print(" Error de conexión:", e)
