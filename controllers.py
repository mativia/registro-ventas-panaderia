from decimal import Decimal
from typing import Optional, Tuple, List
from models import Producto, Venta, RegistroVentas
from repository import VentasRepository

class VentasController:
    def __init__(self, repository: VentasRepository):
        self.repository = repository
        self.registro = RegistroVentas([])

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

    def generar_pdf(self) -> Tuple[bool, str]:
        if not self.registro.ventas:
            return False, "No hay ventas para guardar"
            
        try:
            nombre_archivo = self.repository.generar_pdf(self.registro)
            self.registro.vaciar()
            return True, f"PDF guardado como {nombre_archivo}"
        except Exception as e:
            return False, f"Error al generar PDF: {str(e)}"

    @property
    def total_actual(self) -> Decimal:
        return self.registro.total_dia 