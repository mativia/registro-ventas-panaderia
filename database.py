# database.py
import sqlite3

DB_NAME = "panaderia.db"  # nombre del archivo de la base de datos

def get_connection():
    """Devuelve una conexión a la base de datos SQLite"""
    return sqlite3.connect(DB_NAME)

def create_tables():
    """Crea las tablas productos y ventas si no existen"""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                unidad TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        """)

        conn.commit()

if __name__ == "__main__":
    create_tables()
    print("¡Base de datos y tablas creadas correctamente!")
