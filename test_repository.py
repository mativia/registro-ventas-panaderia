# test_repository.py
from repository import Repository
from models import Producto

def main():
    repo = Repository()

    print("➡️ Agregando producto: Pan")
    producto_pan = Producto("Pan", 1500, "kg")
    repo.agregar_producto(producto_pan)
    print("✅ Producto agregado.")

    print("\n➡️ Listando productos en base de datos:")
    productos = repo.obtener_productos()
    for p in productos:
        print(f"ID: {p.id} | Nombre: {p.nombre} | Precio: {p.precio} | Unidad: {p.unidad}")

    if productos:
        primer_id = productos[0].id
        print(f"\n➡️ Editando el primer producto (ID {primer_id})...")
        repo.editar_producto(primer_id, "Pan Integral", 1800, "kg")
        print("✅ Producto editado.")

        print("\n➡️ Productos actualizados:")
        productos = repo.obtener_productos()
        for p in productos:
            print(f"ID: {p.id} | Nombre: {p.nombre} | Precio: {p.precio} | Unidad: {p.unidad}")

        print(f"\n➡️ Eliminando el producto (ID {primer_id})...")
        repo.eliminar_producto(primer_id)
        print("✅ Producto eliminado.")

        print("\n➡️ Productos tras eliminación:")
        productos = repo.obtener_productos()
        for p in productos:
            print(f"ID: {p.id} | Nombre: {p.nombre} | Precio: {p.precio} | Unidad: {p.unidad}")
    else:
        print("\n⚠️ No hay productos en la base para editar o eliminar.")

if __name__ == "__main__":
    main()
