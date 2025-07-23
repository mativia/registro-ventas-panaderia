from controllers import VentasController
from repository import Repository

def main():
    controller = VentasController(Repository())

    print("➡️ Agregando productos de prueba...")
    controller.add_producto("Pan", "1500", "kg")
    controller.add_producto("Factura", "300", "unidad")
    controller.add_producto("Criollo", "4000", "kg")
    print("✅ Productos agregados.")

    print("\n➡️ Listando productos actuales:")
    productos = controller.get_productos()
    for p in productos:
        print(f"ID: {p.id} | Nombre: {p.nombre} | Precio: {p.precio} | Unidad: {p.unidad}")

    print("\n➡️ Registrando ventas simuladas...")
    success, msg, venta1 = controller.procesar_venta("Pan", 2.5)
    success, msg, venta2 = controller.procesar_venta("Factura", 10)

    if venta1 and venta2:
        print(f" - Venta registrada: {venta1.cantidad} kg de {venta1.producto.nombre}")
        print(f" - Venta registrada: {venta2.cantidad} unidades de {venta2.producto.nombre}")
        print(f"Total actual del ticket: ${controller.total_actual:.2f}")
    else:
        print("⚠️ Error al registrar ventas.")

    print("\n➡️ Confirmando venta y registrando en la base de datos...")
    controller.registrar_venta_actual()
    print("✅ Ventas registradas.")

    print("\n➡️ Ventas totales registradas en la base de datos:")
    ventas_del_dia = controller.repository.obtener_ventas()
    for v in ventas_del_dia:
        print(f"ID: {v.id} | Producto: {v.producto.nombre} | Cantidad: {v.cantidad} | Fecha: {v.fecha}")

if __name__ == "__main__":
    main()
