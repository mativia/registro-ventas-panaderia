import tkinter as tk
from tkinter import ttk, messagebox
from controllers import VentasController

class VentasView:
    def __init__(self, controller: VentasController):
        self.controller = controller
        self.ventana = tk.Tk()
        self.ventana.title("Registro de Ventas - Panadería")
        self.ventana.geometry("520x620")
        self._init_ui()

    def _init_ui(self):
        # Producto
        tk.Label(self.ventana, text="Producto:").pack()
        self.combo_producto = ttk.Combobox(
            self.ventana, 
            values=[p.nombre for p in self.controller.get_productos()]
        )
        self.combo_producto.pack()
        self.combo_producto.bind("<<ComboboxSelected>>", self._actualizar_info_producto)

        # Info del producto
        frame_info = tk.Frame(self.ventana)
        frame_info.pack(pady=5)

        tk.Label(frame_info, text="Precio: ").grid(row=0, column=0, sticky="e")
        self.label_precio = tk.Label(frame_info, text="-")
        self.label_precio.grid(row=0, column=1, sticky="w")

        tk.Label(frame_info, text="Unidad: ").grid(row=1, column=0, sticky="e")
        self.label_unidad = tk.Label(frame_info, text="-")
        self.label_unidad.grid(row=1, column=1, sticky="w")

        # Cantidad
        tk.Label(self.ventana, text="Cantidad:").pack()
        self.entry_cantidad = tk.Entry(self.ventana)
        self.entry_cantidad.pack()

        # Frame principal horizontal
        frame_ventas = tk.Frame(self.ventana)
        frame_ventas.pack(pady=10)

        # Lista de ventas (izquierda)
        self.lista_ventas = tk.Listbox(frame_ventas, width=50, height=10)
        self.lista_ventas.grid(row=0, column=0, rowspan=2, padx=(10, 0), pady=5)

        # Botones Agregar y Eliminar (derecha)
        btn_add = tk.Button(
            frame_ventas, 
            text="Agregar", 
            command=self._agregar_venta, 
            width=10, 
            height=2
        )
        btn_add.grid(row=0, column=1, padx=10, pady=(10, 5))

        btn_delete = tk.Button(
            frame_ventas, 
            text="Eliminar", 
            command=self._eliminar_venta, 
            width=10, 
            height=2
        )
        btn_delete.grid(row=1, column=1, padx=10, pady=(5, 10))

        # Frame inferior para VACÍO + TOTAL
        frame_inferior = tk.Frame(self.ventana)
        frame_inferior.pack(fill="x", padx=10, pady=5)

        btn_vaciar = tk.Button(
            frame_inferior, 
            text="Vaciar", 
            command=self._vaciar_ticket, 
            width=8, 
            height=2
        )
        btn_vaciar.pack(side="left")

        self.label_total = tk.Label(
            frame_inferior, 
            text="Total actual: $0.00", 
            font=("Arial", 12, "bold")
        )
        self.label_total.pack(side="right")

        # Botón generar PDF
        tk.Button(
            self.ventana, 
            text="Generar PDF del día", 
            command=self._generar_pdf, 
            height=2, 
            width=30
        ).pack(pady=10)

    def _actualizar_info_producto(self, event):
        nombre = self.combo_producto.get()
        producto = self.controller.repository.get_producto_by_nombre(nombre)
        if producto:
            self.label_precio.config(text=f"${producto.precio:.2f}")
            self.label_unidad.config(text=producto.unidad)

    def _actualizar_total(self):
        self.label_total.config(
            text=f"Total actual: ${self.controller.total_actual:.2f}"
        )

    def _agregar_venta(self):
        nombre = self.combo_producto.get()
        cantidad_txt = self.entry_cantidad.get()

        try:
            cantidad = float(cantidad_txt)
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida.")
            return

        success, mensaje, venta = self.controller.procesar_venta(nombre, cantidad)
        
        if not success:
            messagebox.showerror("Error", mensaje)
            return

        self.lista_ventas.insert(
            tk.END, 
            f"{venta.producto.nombre} - {venta.cantidad} {venta.producto.unidad} "
            f"x ${venta.producto.precio:.2f} = ${venta.total:.2f}"
        )

        # Limpiar campos
        self.entry_cantidad.delete(0, tk.END)
        self.combo_producto.set("")
        self.label_precio.config(text="-")
        self.label_unidad.config(text="-")
        self._actualizar_total()

    def _eliminar_venta(self):
        seleccion = self.lista_ventas.curselection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia", 
                "Seleccioná un producto para eliminar."
            )
            return

        index = seleccion[0]
        if self.controller.eliminar_venta(index):
            self.lista_ventas.delete(index)
            self._actualizar_total()

    def _vaciar_ticket(self):
        confirmacion = messagebox.askyesno(
            "Confirmar", 
            "¿Estás seguro que querés eliminar todo el ticket del día?"
        )
        if confirmacion:
            self.controller.vaciar_registro()
            self.lista_ventas.delete(0, tk.END)
            self._actualizar_total()

    def _generar_pdf(self):
        success, mensaje = self.controller.generar_pdf()
        if success:
            messagebox.showinfo("PDF generado", mensaje)
            self.lista_ventas.delete(0, tk.END)
            self._actualizar_total()
        else:
            messagebox.showinfo("Sin datos", mensaje)

    def run(self):
        self.ventana.mainloop() 