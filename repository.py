# repository.py
from database import get_connection
from models import Producto, Venta
from datetime import datetime

class Repository:
    
    def get_producto_by_nombre(self, nombre):
        """Devuelve un producto por su nombre, o None si no existe"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, precio, unidad FROM productos WHERE nombre=?", (nombre,))
            row = cursor.fetchone()
            if row:
                producto = Producto(row[1], row[2], row[3])
                producto.id = row[0]
                return producto
            return None


    def agregar_producto(self, producto):
        """Agrega un producto a la base de datos"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, precio, unidad) VALUES (?, ?, ?)",
                (producto.nombre, producto.precio, producto.unidad)
            )
            conn.commit()

    def obtener_productos(self):
        """Obtiene todos los productos de la base de datos"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, precio, unidad FROM productos")
            rows = cursor.fetchall()
            productos = []
            for row in rows:
                p = Producto(row[1], row[2], row[3])
                p.id = row[0]
                productos.append(p)
            return productos

    def editar_producto(self, producto_id, nuevo_nombre, nuevo_precio, nueva_unidad):
        """Edita un producto existente"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE productos SET nombre=?, precio=?, unidad=? WHERE id=?",
                (nuevo_nombre, nuevo_precio, nueva_unidad, producto_id)
            )
            conn.commit()

    def eliminar_producto(self, producto_id):
        """Elimina un producto de la base de datos"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id=?", (producto_id,))
            conn.commit()

    def registrar_venta(self, producto_id, cantidad):
        """Registra una venta"""
        with get_connection() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO ventas (producto_id, cantidad, fecha) VALUES (?, ?, ?)",
                (producto_id, cantidad, fecha_actual)
            )
            conn.commit()

    def obtener_ventas(self):
        """Obtiene todas las ventas registradas"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ventas.id, productos.nombre, ventas.cantidad, ventas.fecha
                FROM ventas
                JOIN productos ON ventas.producto_id = productos.id
            """)
            rows = cursor.fetchall()
            ventas = []
            for row in rows:
                venta = Venta(Producto(row[1], 0, ""), row[2], row[3])
                venta.id = row[0]
                ventas.append(venta)
            return ventas

    def editar_venta(self, venta_id, producto_id, cantidad, fecha):
        """Edita una venta existente en la base de datos"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE ventas SET producto_id=?, cantidad=?, fecha=? WHERE id=?",
                (producto_id, cantidad, fecha, venta_id)
            )
            conn.commit()

    def eliminar_venta(self, venta_id):
        """Elimina una venta de la base de datos"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ventas WHERE id=?", (venta_id,))
            conn.commit()
