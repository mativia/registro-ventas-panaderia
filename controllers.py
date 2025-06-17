from decimal import Decimal
from typing import Optional, Tuple, List
from models import Producto, Venta, RegistroVentas
from repository import VentasRepository

class VentasController:
    def __init__(self, repository: VentasRepository):
        self.repository = repository
        self.registro = RegistroVentas([])
        self.ventas_del_dia = []  # Lista para almacenar todas las ventas del día

    def get_productos(self) -> List[Producto]:
        return self.repository.get_productos()

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

            # Insertar producto
            producto = self.repository.insert_producto(nombre, precio_decimal, unidad)
            return True, "Producto agregado exitosamente", producto

        except ValueError as e:
            return False, str(e), None
        except Exception as e:
            return False, f"Error al agregar el producto: {str(e)}", None

    def update_producto(self, id: int, nombre: str, precio: str, unidad: str) -> Tuple[bool, str, Optional[Producto]]:
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

            # Actualizar producto
            producto = self.repository.update_producto(id, nombre, precio_decimal, unidad)
            if producto is None:
                return False, "Producto no encontrado", None
                
            return True, "Producto actualizado exitosamente", producto

        except ValueError as e:
            return False, str(e), None
        except Exception as e:
            return False, f"Error al actualizar el producto: {str(e)}", None

    def delete_producto(self, id: int) -> Tuple[bool, str]:
        try:
            if self.repository.delete_producto(id):
                return True, "Producto eliminado exitosamente"
            return False, "Producto no encontrado"
        except Exception as e:
            return False, f"Error al eliminar el producto: {str(e)}"

    def procesar_venta(self, nombre_producto: str, cantidad: float) -> Tuple[bool, str, Optional[Venta]]:
        if not nombre_producto or cantidad <= 0:
            return False, "Datos de venta inválidos", None

        producto = self.repository.get_producto_by_nombre(nombre_producto)
        if not producto:
            return False, "Producto no encontrado", None

        total = producto.precio * Decimal(str(cantidad))
        venta = Venta(producto, cantidad, total)
        self.registro.agregar_venta(venta)
        
        return True, "", venta

    def eliminar_venta(self, index: int) -> bool:
        if 0 <= index < len(self.registro.ventas):
            self.registro.eliminar_venta(index)
            return True
        return False

    def vaciar_registro(self):
        self.registro.vaciar()

    def registrar_venta_actual(self):
        """Registra la venta actual en el historial del día"""
        if self.registro.ventas:
            # Crear una copia de las ventas actuales
            venta_actual = self.registro.ventas.copy()
            # Agregar al historial del día
            self.ventas_del_dia.extend(venta_actual)
            # Limpiar el registro actual
            self.registro.vaciar()
            print(f"Venta registrada. Total de ventas del día: {len(self.ventas_del_dia)}")  # Debug

    def cerrar_caja(self, turno: str) -> Tuple[bool, str]:
        print(f"Intentando cerrar caja. Ventas del día: {len(self.ventas_del_dia)}")  # Debug
        if not self.ventas_del_dia:
            return False, "No hay ventas para guardar"
            
        try:
            # Crear un registro temporal con todas las ventas del día
            registro_dia = RegistroVentas(self.ventas_del_dia)
            nombre_archivo = self.repository.generar_excel(registro_dia, turno)
            # Limpiar el historial después de guardar
            self.ventas_del_dia.clear()
            return True, f"Excel {turno} generado como {nombre_archivo}"
        except Exception as e:
            return False, f"Error al generar Excel: {str(e)}"

    @property
    def total_actual(self) -> Decimal:
        return self.registro.total_dia

    def get_ultima_venta(self) -> Optional[Venta]:
        """Obtiene la última venta registrada"""
        if self.registro.ventas:
            return self.registro.ventas[-1]
        return None

    def generar_ticket(self, venta: Venta) -> str:
        """Genera un ticket PDF para una venta individual"""
        if not venta:
            raise ValueError("No hay venta para generar el ticket")
            
        try:
            return self.repository.generar_ticket(venta)
        except Exception as e:
            raise Exception(f"Error al generar el ticket: {str(e)}") 