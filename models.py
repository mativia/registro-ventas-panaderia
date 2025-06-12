from dataclasses import dataclass
from typing import List
from decimal import Decimal

@dataclass
class Producto:
    nombre: str
    precio: Decimal
    unidad: str

@dataclass
class Venta:
    producto: Producto
    cantidad: float
    total: Decimal

@dataclass
class RegistroVentas:
    ventas: List[Venta]
    total_dia: Decimal = Decimal('0')

    def agregar_venta(self, venta: Venta):
        self.ventas.append(venta)
        self.total_dia += venta.total

    def eliminar_venta(self, index: int):
        venta = self.ventas.pop(index)
        self.total_dia -= venta.total

    def vaciar(self):
        self.ventas.clear()
        self.total_dia = Decimal('0') 