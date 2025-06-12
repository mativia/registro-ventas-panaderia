from decimal import Decimal
from typing import Optional, Tuple
from models import Producto, Venta, RegistroVentas
from repository import VentasRepository

class VentasController:
    def __init__(self, repository: VentasRepository):
        self.repository = repository
        self.registro = RegistroVentas([])

    def get_productos(self):
        return self.repository.get_productos()

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