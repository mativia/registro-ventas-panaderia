from decimal import Decimal
from datetime import datetime
from fpdf import FPDF
from typing import List, Optional
from models import Producto, Venta, RegistroVentas

class VentasRepository:
    def __init__(self):
        self._next_id = 1
        self.productos = [
            Producto("Pan", Decimal('1500'), "kg", self._get_next_id()),
            Producto("Criollo salado", Decimal('4000'), "kg", self._get_next_id()),
            Producto("Criollo dulce", Decimal('4200'), "kg", self._get_next_id()),
            Producto("Torta", Decimal('10000'), "kg", self._get_next_id()),
            Producto("Canoncito de dulce de leche", Decimal('300'), "unidad", self._get_next_id()),
            Producto("Brownie", Decimal('800'), "unidad", self._get_next_id()),
            Producto("Alfajor chocolate", Decimal('1000'), "unidad", self._get_next_id()),
            Producto("Pan negro", Decimal('3000'), "kg", self._get_next_id()),
            Producto("Roscas Pascuas", Decimal('3000'), "unidad", self._get_next_id()),
            Producto("Alfajor maizena chico", Decimal('500'), "unidad", self._get_next_id()),
            Producto("Alfajor maizena grande", Decimal('850'), "unidad", self._get_next_id()),
            Producto("Factura", Decimal('300'), "unidad", self._get_next_id()),
        ]

    def _get_next_id(self) -> int:
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def get_productos(self) -> List[Producto]:
        return self.productos.copy()

    def get_producto_by_nombre(self, nombre: str) -> Optional[Producto]:
        return next((p for p in self.productos if p.nombre == nombre), None)

    def get_producto_by_id(self, id: int) -> Optional[Producto]:
        return next((p for p in self.productos if p.id == id), None)

    def insert_producto(self, nombre: str, precio: Decimal, unidad: str) -> Producto:
        # Validar que no exista otro producto con el mismo nombre
        if self.get_producto_by_nombre(nombre):
            raise ValueError(f"Ya existe un producto con el nombre '{nombre}'")
        
        nuevo_producto = Producto(nombre, precio, unidad, self._get_next_id())
        self.productos.append(nuevo_producto)
        return nuevo_producto

    def update_producto(self, id: int, nombre: str, precio: Decimal, unidad: str) -> Optional[Producto]:
        producto = self.get_producto_by_id(id)
        if not producto:
            return None
        
        # Si el nombre cambió, verificar que no exista otro producto con ese nombre
        if nombre != producto.nombre and self.get_producto_by_nombre(nombre):
            raise ValueError(f"Ya existe un producto con el nombre '{nombre}'")
        
        # Actualizar el producto
        index = self.productos.index(producto)
        producto_actualizado = Producto(nombre, precio, unidad, id)
        self.productos[index] = producto_actualizado
        return producto_actualizado

    def delete_producto(self, id: int) -> bool:
        producto = self.get_producto_by_id(id)
        if producto:
            self.productos.remove(producto)
            return True
        return False

    def generar_pdf(self, registro: RegistroVentas) -> str:
        fecha = datetime.now().strftime("%Y-%m-%d")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Ventas del día {fecha}", ln=True, align="C")
        pdf.ln(10)

        for venta in registro.ventas:
            linea = (f"{venta.producto.nombre} - {venta.cantidad} "
                    f"{venta.producto.unidad} x ${venta.producto.precio:.2f} = "
                    f"${venta.total:.2f}")
            pdf.cell(200, 10, txt=linea, ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=f"TOTAL DEL DÍA: ${registro.total_dia:.2f}", ln=True)

        nombre_archivo = f"Ventas_{fecha}.pdf"
        pdf.output(nombre_archivo)
        return nombre_archivo 