from decimal import Decimal
from typing import Optional, Tuple, List
from models import Producto, Venta
from repository import Repository

class VentasController:
    def __init__(self, repository: Repository):
        self.repository = repository
        self.ventas_actuales = [] # Ventas cargadas en el ticket actual
        self.ventas_del_dia = [] 
#Obtener productos de la base de datos
    def get_productos(self) -> List[Producto]:
        return self.repository.obtener_productos()

#Agregar productos nuevos a la base de datos
    def add_producto(self, nombre: str, precio: str, unidad: str) -> Tuple[bool, str, Optional[Producto]]:
        try:
            # Validaciones
            if not nombre or not precio or not unidad:
                return False, "Todos los campos son requeridos", None
            
            try:
                precio_decimal = Decimal(precio)
                if precio_decimal <= 0:
                    return False, "El precio debe ser mayor a 0", None
            except:
                return False, "El precio debe ser un número válido", None

            if unidad not in ["kg", "unidad"]:
                return False, "La unidad debe ser 'kg' o 'unidad'", None

            producto = Producto(nombre, float(precio_decimal), unidad)
            self.repository.agregar_producto(producto)
            return True, "Producto agregado exitosamente", producto

        except Exception as e:
            return False, f"Error al agregar el producto: {str(e)}", None
#Actualizar productos existentes
    def update_producto(self, id: int, nombre: str, precio: str, unidad: str) -> Tuple[bool, str, Optional[Producto]]:
        try:
            if not nombre or not precio or not unidad:
                return False, "Todos los campos son requeridos", None
            
            try:
                precio_decimal = Decimal(precio)
                if precio_decimal <= 0:
                    return False, "El precio debe ser mayor a 0", None
            except:
                return False, "El precio debe ser un número válido", None

            if unidad not in ["kg", "unidad"]:
                return False, "La unidad debe ser 'kg' o 'unidad'", None

            self.repository.editar_producto(id, nombre, float(precio_decimal), unidad)
            return True, "Producto actualizado exitosamente", None

        except Exception as e:
            return False, f"Error al actualizar el producto: {str(e)}", None
#Eliminar productos de la base de datos
    def delete_producto(self, id: int) -> Tuple[bool, str]:
        try:
            self.repository.eliminar_producto(id)
            return True, "Producto eliminado exitosamente"
        except Exception as e:
            return False, f"Error al eliminar el producto: {str(e)}"
#Agregar productos al carrito
    def procesar_venta(self, nombre_producto: str, cantidad: float) -> Tuple[bool, str, Optional[Venta]]:
        if not nombre_producto or cantidad <= 0:
            return False, "Datos de venta inválidos", None

        producto = self.repository.get_producto_by_nombre(nombre_producto)
        if not producto:
            return False, "Producto no encontrado", None

        total = Decimal(str(cantidad)) * Decimal(str(producto.precio))
        venta = Venta(producto, cantidad,None, total)
        self.ventas_actuales.append(venta)
        
        return True, "", venta
#Eliminar productos del carrito
    def eliminar_venta(self, index: int) -> bool:
        if 0 <= index < len(self.ventas_actuales):
            self.ventas_actuales.pop(index)
            return True
        return False
#Vaciar el carrito
    def vaciar_registro(self):
        self.ventas_actuales.clear()
#Registrar la venta actual
    def registrar_venta_actual(self):
        """Registra las ventas actuales en la base de datos"""
        if self.ventas_actuales:
            for venta in self.ventas_actuales:
                self.repository.registrar_venta(venta.producto.id, venta.cantidad)
            self.ventas_actuales.clear()
            print(f"Venta registrada en la base de datos.")

    def cerrar_caja(self, turno: str) -> Tuple[bool, str]:
        ventas_del_dia = self.repository.obtener_ventas()
        if not ventas_del_dia:
            return False, "No hay ventas registradas para cerrar caja."
        
        total_dia = sum(Decimal(venta.cantidad) * Decimal(venta.producto.precio) for venta in ventas_del_dia)
        mensaje = f"Turno {turno.capitalize()} cerrado. Total de ventas: ${total_dia:.2f}"
        return True, mensaje

    @property
    def total_actual(self) -> Decimal:
        return sum(Decimal(venta.total) for venta in self.ventas_actuales)

    def get_ultima_venta(self) -> Optional[Venta]:
        """Obtiene la última venta registrada en el ticket actual"""
        if self.ventas_actuales:
            return self.ventas_actuales[-1]
        return None

    def get_ventas_en_bd(self):
        """Devuelve todas las ventas guardadas en la base de datos"""
        return self.repository.obtener_ventas()

    def update_venta_en_bd(self, venta_id, producto_id, cantidad, fecha):
        """Actualiza una venta existente en la base de datos"""
        try:
            self.repository.editar_venta(venta_id, producto_id, cantidad, fecha)
            return True, "Venta actualizada exitosamente"
        except Exception as e:
            return False, f"Error al actualizar la venta: {str(e)}"

    def delete_venta_en_bd(self, venta_id):
        """Elimina una venta de la base de datos"""
        try:
            self.repository.eliminar_venta(venta_id)
            return True, "Venta eliminada exitosamente"
        except Exception as e:
            return False, f"Error al eliminar la venta: {str(e)}"
