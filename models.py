class Producto:
    def __init__(self, nombre, precio, unidad):
        self.id = None  # ID en la base de datos (se asigna al obtenerlo)
        self.nombre = nombre
        self.precio = precio
        self.unidad = unidad

class Venta:
    def __init__(self, producto, cantidad, fecha=None, total=None):
        self.id = None
        self.producto = producto
        self.cantidad = cantidad
        self.fecha = fecha
        self.total = total


