from decimal import Decimal
from datetime import datetime
from fpdf import FPDF
from typing import List
from models import Producto, Venta, RegistroVentas

class VentasRepository:
    def __init__(self):
        self.productos = [
            Producto("Pan", Decimal('1500'), "kg"),
            Producto("Criollo salado", Decimal('4000'), "kg"),
            Producto("Criollo dulce", Decimal('4200'), "kg"),
            Producto("Torta", Decimal('10000'), "kg"),
            Producto("Canoncito de dulce de leche", Decimal('300'), "unidad"),
            Producto("Brownie", Decimal('800'), "unidad"),
            Producto("Alfajor chocolate", Decimal('1000'), "unidad"),
            Producto("Pan negro", Decimal('3000'), "kg"),
            Producto("Roscas Pascuas", Decimal('3000'), "unidad"),
            Producto("Alfajor maizena chico", Decimal('500'), "unidad"),
            Producto("Alfajor maizena grande", Decimal('850'), "unidad"),
            Producto("Factura", Decimal('300'), "unidad"),
        ]

    def get_productos(self) -> List[Producto]:
        return self.productos

    def get_producto_by_nombre(self, nombre: str) -> Producto:
        return next((p for p in self.productos if p.nombre == nombre), None)

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