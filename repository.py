from decimal import Decimal
from datetime import datetime
from typing import List, Optional, Dict
from models import Producto, Venta, RegistroVentas
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
import os

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

    def generar_excel(self, ventas: List[Dict], turno: str) -> str:
        """Genera un archivo Excel con las ventas del día"""
        try:
            # Crear directorio si no existe
            os.makedirs("ventas", exist_ok=True)
            
            # Generar nombre del archivo con fecha y turno
            fecha = datetime.now().strftime("%Y-%m-%d")
            nombre_archivo = f"ventas/ventas_{fecha}_{turno}.xlsx"
            
            # Crear un nuevo libro de Excel
            wb = Workbook()
            ws = wb.active
            ws.title = "Ventas"
            
            # Escribir encabezados
            ws.append([
                "Fecha",
                "Hora",
                "Producto",
                "Cantidad",
                "Precio Unitario",
                "Subtotal"
            ])
            
            # Escribir datos
            total_caja = 0
            for venta in ventas:
                for item in venta['items']:
                    subtotal = item['cantidad'] * item['precio']
                    total_caja += subtotal
                    ws.append([
                        venta['fecha'],
                        venta['hora'],
                        item['producto'],
                        item['cantidad'],
                        item['precio'],
                        subtotal
                    ])
            
            # Agregar fila con el total
            ws.append([])  # Línea en blanco
            ws.append(["", "", "", "", "Total Caja:", total_caja])
            
            # Ajustar ancho de columnas
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                ws.column_dimensions[column].width = adjusted_width
            
            # Guardar archivo
            wb.save(nombre_archivo)
            return nombre_archivo
            
        except Exception as e:
            print(f"Error al generar Excel: {str(e)}")
            raise 