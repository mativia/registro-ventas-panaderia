import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF
from datetime import datetime

# Lista de productos
productos = [
    {"nombre": "Pan", "precio": 1500, "unidad": "kg"},
    {"nombre": "Criollo salado", "precio": 4000, "unidad": "kg"},
    {"nombre": "Criollo dulce", "precio": 4200, "unidad": "kg"},
    {"nombre": "Torta", "precio": 10000, "unidad": "kg"},
    {"nombre": "Canoncito de dulce de leche", "precio": 300, "unidad": "unidad"},
    {"nombre": "Brownie", "precio": 800, "unidad": "unidad"},
    {"nombre": "Alfajor chocolate", "precio": 1000, "unidad": "unidad"},
    {"nombre": "Pan negro", "precio": 3000, "unidad": "kg"},
    {"nombre": "Roscas Pascuas", "precio": 3000, "unidad": "unidad"},
    {"nombre": "Alfajor maizena chico", "precio": 500, "unidad": "unidad"},
    {"nombre": "Alfajor maizena grande", "precio": 850, "unidad": "unidad"},
    {"nombre": "Factura", "precio": 300, "unidad": "unidad"},
]

ventas = []
total_actual = 0.0

# Función para actualizar la info al seleccionar un producto
def actualizar_info_producto(event):
    nombre = combo_producto.get()
    for p in productos:
        if p["nombre"] == nombre:
            label_precio.config(text=f"${p['precio']:.2f}")
            label_unidad.config(text=p["unidad"])
            break

# Función para actualizar el total actual
def actualizar_total():
    total = sum(v[4] for v in ventas)
    global total_actual
    total_actual = total
    label_total.config(text=f"Total actual: ${total:.2f}")

# Función para agregar venta
def agregar_venta():
    nombre = combo_producto.get()
    cantidad_txt = entry_cantidad.get()

    if not nombre or not cantidad_txt:
        messagebox.showwarning("Error", "Completá todos los campos.")
        return

    try:
        cantidad = float(cantidad_txt)
    except ValueError:
        messagebox.showerror("Error", "Cantidad inválida.")
        return

    producto = next((p for p in productos if p["nombre"] == nombre), None)
    if not producto:
        messagebox.showerror("Error", "Producto no encontrado.")
        return

    precio_unitario = producto["precio"]
    unidad = producto["unidad"]
    total = precio_unitario * cantidad
    ventas.append((nombre, cantidad, unidad, precio_unitario, total))
    lista_ventas.insert(tk.END, f"{nombre} - {cantidad} {unidad} x ${precio_unitario:.2f} = ${total:.2f}")

    # Limpiar campos
    entry_cantidad.delete(0, tk.END)
    combo_producto.set("")
    label_precio.config(text="-")
    label_unidad.config(text="-")
    actualizar_total()

# Función para eliminar producto seleccionado
def eliminar_venta():
    seleccion = lista_ventas.curselection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccioná un producto para eliminar.")
        return

    index = seleccion[0]
    lista_ventas.delete(index)
    ventas.pop(index)
    actualizar_total()

# Función para vaciar todo el ticket
def vaciar_ticket():
    confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro que querés eliminar todo el ticket del día?")
    if confirmacion:
        lista_ventas.delete(0, tk.END)
        ventas.clear()
        actualizar_total()

# Función para generar PDF
def generar_pdf():
    if not ventas:
        messagebox.showinfo("Sin datos", "No hay ventas para guardar.")
        return

    fecha = datetime.now().strftime("%Y-%m-%d")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Ventas del día {fecha}", ln=True, align="C")
    pdf.ln(10)

    total_dia = 0
    for v in ventas:
        linea = f"{v[0]} - {v[1]} {v[2]} x ${v[3]:.2f} = ${v[4]:.2f}"
        pdf.cell(200, 10, txt=linea, ln=True)
        total_dia += v[4]

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"TOTAL DEL DÍA: ${total_dia:.2f}", ln=True)

    nombre_archivo = f"Ventas_{fecha}.pdf"
    pdf.output(nombre_archivo)
    messagebox.showinfo("PDF generado", f"Guardado como {nombre_archivo}")
    ventas.clear()
    lista_ventas.delete(0, tk.END)
    actualizar_total()

# Interfaz
ventana = tk.Tk()
ventana.title("Registro de Ventas - Panadería")
ventana.geometry("520x620")

# Producto
tk.Label(ventana, text="Producto:").pack()
combo_producto = ttk.Combobox(ventana, values=[p["nombre"] for p in productos])
combo_producto.pack()
combo_producto.bind("<<ComboboxSelected>>", actualizar_info_producto)

# Info del producto
frame_info = tk.Frame(ventana)
frame_info.pack(pady=5)

tk.Label(frame_info, text="Precio: ").grid(row=0, column=0, sticky="e")
label_precio = tk.Label(frame_info, text="-")
label_precio.grid(row=0, column=1, sticky="w")

tk.Label(frame_info, text="Unidad: ").grid(row=1, column=0, sticky="e")
label_unidad = tk.Label(frame_info, text="-")
label_unidad.grid(row=1, column=1, sticky="w")

# Cantidad
tk.Label(ventana, text="Cantidad:").pack()
entry_cantidad = tk.Entry(ventana)
entry_cantidad.pack()

# Frame principal horizontal
frame_ventas = tk.Frame(ventana)
frame_ventas.pack(pady=10)

# Lista de ventas (izquierda)
lista_ventas = tk.Listbox(frame_ventas, width=50, height=10)
lista_ventas.grid(row=0, column=0, rowspan=2, padx=(10, 0), pady=5)

# Cargar íconos
##icono_add = tk.PhotoImage(file="add.png")
##icono_delete = tk.PhotoImage(file="delete.png")

# Botones [+] y [-] (derecha)
btn_add = tk.Button(frame_ventas,  command=agregar_venta, width=40, height=40)
btn_add.grid(row=0, column=1, padx=10, pady=(10, 5))

btn_delete = tk.Button(frame_ventas, command=eliminar_venta, width=40, height=40)
btn_delete.grid(row=1, column=1, padx=10, pady=(5, 10))

# Frame inferior para VACÍO + TOTAL
frame_inferior = tk.Frame(ventana)
frame_inferior.pack(fill="x", padx=10, pady=5)

btn_vaciar = tk.Button(frame_inferior, text="Vaciar", command=vaciar_ticket, width=8, height=2)
btn_vaciar.pack(side="left")

label_total = tk.Label(frame_inferior, text="Total actual: $0.00", font=("Arial", 12, "bold"))
label_total.pack(side="right")

# Botón generar PDF (separado al final)
tk.Button(ventana, text="Generar PDF del día", command=generar_pdf, height=2, width=30).pack(pady=10)

# Mantener iconos en memoria


ventana.mainloop()


