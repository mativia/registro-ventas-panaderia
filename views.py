import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from controllers import VentasController




class VentasView:
    def __init__(self, controller: VentasController):
        self.controller = controller
        self.ventana = ttk.Window(
            title="Sistema de Ventas - Panadería",
            themename="cosmo",
            resizable=(True, True)
        )
        self.ventana.geometry("1600x900")
        self.ventana.minsize(1280, 800)
        
        # Centrar la ventana en la pantalla
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()
        x = (screen_width - 1600) // 2
        y = (screen_height - 900) // 2
        self.ventana.geometry(f"1600x900+{x}+{y}")
        
        self._init_ui()

    def _init_ui(self):
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=5)

        # Pestaña de Ventas
        self.tab_ventas = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.tab_ventas, text="Ventas")
        self._init_ui_ventas()

        # Pestaña de Productos
        self.tab_productos = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.tab_productos, text="Productos")
        self._init_ui_productos()

        # Pestaña de Ventas en BD
        self.tab_ventas_bd = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.tab_ventas_bd, text="Ventas en BD")
        self._init_ui_ventas_bd()

    def _init_ui_ventas(self):
        # Título
        titulo = ttk.Label(
            self.tab_ventas,
            text="Registro de Ventas",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        )
        titulo.pack(pady=10)

        # Frame para selección de producto
        producto_frame = ttk.LabelFrame(
            self.tab_ventas,
            text="Selección de Producto",
            padding=15,
            bootstyle="primary"
        )
        producto_frame.pack(fill=X, pady=10)

        # Grid para productos más vendidos
        productos_grid = ttk.Frame(producto_frame)
        productos_grid.pack(fill=X, pady=10)
        self._crear_botones_productos(productos_grid)

        # Combobox y cantidad
        input_frame = ttk.Frame(producto_frame)
        input_frame.pack(fill=X)

        # Producto
        producto_select_frame = ttk.Frame(input_frame)
        producto_select_frame.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
        
        ttk.Label(
            producto_select_frame,
            text="Producto:",
            font=("Helvetica", 10)
        ).pack(anchor=W)
        
        self.combo_producto = ttk.Combobox(
            producto_select_frame,
            values=[p.nombre for p in self.controller.get_productos()],
            bootstyle="primary"
        )
        self.combo_producto.pack(fill=X)
        self.combo_producto.bind("<<ComboboxSelected>>", self._actualizar_info_producto)

        # Cantidad
        cantidad_frame = ttk.Frame(input_frame)
        cantidad_frame.pack(side=LEFT, fill=X, expand=YES)
        
        ttk.Label(
            cantidad_frame,
            text="Cantidad:",
            font=("Helvetica", 10)
        ).pack(anchor=W)
        
        self.entry_cantidad = ttk.Entry(cantidad_frame, bootstyle="primary")
        self.entry_cantidad.pack(fill=X)

        # Info del producto
        info_frame = ttk.Frame(producto_frame)
        info_frame.pack(fill=X, pady=10)

        self.label_precio = ttk.Label(
            info_frame,
            text="Precio: -",
            font=("Helvetica", 12),
            bootstyle="secondary"
        )
        self.label_precio.pack(side=LEFT, padx=5)

        self.label_unidad = ttk.Label(
            info_frame,
            text="Unidad: -",
            font=("Helvetica", 12),
            bootstyle="secondary"
        )
        self.label_unidad.pack(side=LEFT, padx=5)

        # Frame para lista de ventas
        ventas_frame = ttk.LabelFrame(
            self.tab_ventas,
            text="Lista de Ventas",
            padding=15,
            bootstyle="primary"
        )
        ventas_frame.pack(fill=BOTH, expand=YES, pady=10)

        # Lista de ventas con scrollbar
        lista_frame = ttk.Frame(ventas_frame)
        lista_frame.pack(fill=BOTH, expand=YES)

        scrollbar = ttk.Scrollbar(lista_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.lista_ventas = ttk.Treeview(
            lista_frame,
            columns=("producto", "cantidad", "precio", "total"),
            show="headings",
            bootstyle="primary",
            height=8
        )
        
        self.lista_ventas.heading("producto", text="Producto")
        self.lista_ventas.heading("cantidad", text="Cantidad")
        self.lista_ventas.heading("precio", text="Precio Unit.")
        self.lista_ventas.heading("total", text="Total")
        
        self.lista_ventas.column("producto", width=200)
        self.lista_ventas.column("cantidad", width=100)
        self.lista_ventas.column("precio", width=100)
        self.lista_ventas.column("total", width=100)
        
        self.lista_ventas.pack(fill=BOTH, expand=YES)
        
        scrollbar.config(command=self.lista_ventas.yview)
        self.lista_ventas.configure(yscrollcommand=scrollbar.set)

        # Frame para botones de acción
        botones_frame = ttk.Frame(ventas_frame)
        botones_frame.pack(fill=X, pady=(10, 0))

        # Frame para botones principales
        botones_principales = ttk.Frame(botones_frame)
        botones_principales.pack(fill=X, pady=5)

        ttk.Button(
            botones_principales,
            text="Agregar",
            command=self._agregar_venta,
            bootstyle="success",
            width=15
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            botones_principales,
            text="Eliminar",
            command=self._eliminar_venta,
            bootstyle="danger",
            width=15
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            botones_principales,
            text="Vaciar Ticket",
            command=self._vaciar_ticket,
            bootstyle="warning",
            width=15
        ).pack(side=LEFT, padx=5)

        # Frame para botones de caja
        botones_caja = ttk.Frame(botones_frame)
        botones_caja.pack(fill=X, pady=5)

        ttk.Button(
            botones_caja,
            text="Generar Venta",
            command=self._generar_venta,
            bootstyle="success",
            width=25
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            botones_caja,
            text="Cerrar Caja",
            command=self._cerrar_caja,
            bootstyle="primary",
            width=25
        ).pack(side=LEFT, padx=5)

        # Frame inferior
        footer_frame = ttk.Frame(self.tab_ventas)
        footer_frame.pack(fill=X, pady=10)

        # Total
        self.label_total = ttk.Label(
            footer_frame,
            text="Total actual: $0.00",
            font=("Helvetica", 16, "bold"),
            bootstyle="primary"
        )
        self.label_total.pack(side=RIGHT)

    def _init_ui_productos(self):
        # Frame superior para la lista de productos
        lista_frame = ttk.LabelFrame(
            self.tab_productos,
            text="Lista de Productos",
            padding=15,
            bootstyle="primary"
        )
        lista_frame.pack(fill=BOTH, expand=YES, pady=(0, 10))

        # Treeview con scrollbar
        tree_frame = ttk.Frame(lista_frame)
        tree_frame.pack(fill=BOTH, expand=YES)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tree_productos = ttk.Treeview(
            tree_frame,
            columns=("id", "nombre", "precio", "unidad"),
            show="headings",
            bootstyle="primary"
        )
        
        self.tree_productos.heading("id", text="ID")
        self.tree_productos.heading("nombre", text="Nombre")
        self.tree_productos.heading("precio", text="Precio")
        self.tree_productos.heading("unidad", text="Unidad")
        
        self.tree_productos.column("id", width=50)
        self.tree_productos.column("nombre", width=250)
        self.tree_productos.column("precio", width=100)
        self.tree_productos.column("unidad", width=100)
        
        self.tree_productos.pack(fill=BOTH, expand=YES)
        
        scrollbar.config(command=self.tree_productos.yview)
        self.tree_productos.configure(yscrollcommand=scrollbar.set)

        # Frame para formulario
        form_frame = ttk.LabelFrame(
            self.tab_productos,
            text="Gestión de Productos",
            padding=15,
            bootstyle="primary"
        )
        form_frame.pack(fill=X, pady=(0, 10))

        # Campos del formulario
        campos_frame = ttk.Frame(form_frame)
        campos_frame.pack(fill=X, pady=10)

        # Nombre
        nombre_frame = ttk.Frame(campos_frame)
        nombre_frame.pack(side=LEFT, fill=X, expand=YES, padx=5)
        
        ttk.Label(
            nombre_frame,
            text="Nombre:",
            font=("Helvetica", 10)
        ).pack(anchor=W)
        
        self.entry_nombre = ttk.Entry(nombre_frame)
        self.entry_nombre.pack(fill=X)

        # Precio
        precio_frame = ttk.Frame(campos_frame)
        precio_frame.pack(side=LEFT, fill=X, expand=YES, padx=5)
        
        ttk.Label(
            precio_frame,
            text="Precio:",
            font=("Helvetica", 10)
        ).pack(anchor=W)
        
        self.entry_precio = ttk.Entry(precio_frame)
        self.entry_precio.pack(fill=X)

        # Unidad
        unidad_frame = ttk.Frame(campos_frame)
        unidad_frame.pack(side=LEFT, fill=X, expand=YES, padx=5)
        
        ttk.Label(
            unidad_frame,
            text="Unidad:",
            font=("Helvetica", 10)
        ).pack(anchor=W)
        
        self.combo_unidad = ttk.Combobox(
            unidad_frame,
            values=["kg", "unidad"],
            state="readonly"
        )
        self.combo_unidad.pack(fill=X)

        # Botones de acción
        botones_frame = ttk.Frame(form_frame)
        botones_frame.pack(fill=X, pady=(10, 0))

        ttk.Button(
            botones_frame,
            text="Agregar",
            command=self._agregar_producto,
            bootstyle="success",
            width=15
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            botones_frame,
            text="Modificar",
            command=self._modificar_producto,
            bootstyle="warning",
            width=15
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            botones_frame,
            text="Eliminar",
            command=self._eliminar_producto,
            bootstyle="danger",
            width=15
        ).pack(side=LEFT, padx=5)

        # Cargar productos iniciales
        self._cargar_productos()

        # Bind para selección en el tree
        self.tree_productos.bind("<<TreeviewSelect>>", self._on_producto_selected)

    def _init_ui_ventas_bd(self):
        # Frame principal
        frame = ttk.LabelFrame(
            self.tab_ventas_bd,
            text="Ventas guardadas en la base de datos",
            padding=15,
            bootstyle="primary"
        )
        frame.pack(fill=BOTH, expand=YES, pady=(0, 10))

        # Treeview con scrollbar
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=BOTH, expand=YES)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tree_ventas_bd = ttk.Treeview(
            tree_frame,
            columns=("id", "producto", "cantidad", "fecha"),
            show="headings",
            bootstyle="primary"
        )
        self.tree_ventas_bd.heading("id", text="ID Venta")
        self.tree_ventas_bd.heading("producto", text="Producto")
        self.tree_ventas_bd.heading("cantidad", text="Cantidad")
        self.tree_ventas_bd.heading("fecha", text="Fecha")
        self.tree_ventas_bd.column("id", width=80)
        self.tree_ventas_bd.column("producto", width=200)
        self.tree_ventas_bd.column("cantidad", width=100)
        self.tree_ventas_bd.column("fecha", width=200)
        self.tree_ventas_bd.pack(fill=BOTH, expand=YES)
        scrollbar.config(command=self.tree_ventas_bd.yview)
        self.tree_ventas_bd.configure(yscrollcommand=scrollbar.set)

        # Botones de acción
        btn_frame = ttk.Frame(self.tab_ventas_bd)
        btn_frame.pack(fill=X, pady=(10, 0))
        ttk.Button(
            btn_frame,
            text="Refrescar",
            command=self._cargar_ventas_bd,
            bootstyle="primary",
            width=15
        ).pack(side=LEFT, padx=5)
        ttk.Button(
            btn_frame,
            text="Eliminar",
            command=self._eliminar_venta_bd,
            bootstyle="danger",
            width=15
        ).pack(side=LEFT, padx=5)
        ttk.Button(
            btn_frame,
            text="Modificar",
            command=self._modificar_venta_bd,
            bootstyle="warning",
            width=15
        ).pack(side=LEFT, padx=5)

        self._cargar_ventas_bd()

    def _cargar_productos(self):
        # Limpiar tree
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        # Cargar productos
        for producto in self.controller.get_productos():
            self.tree_productos.insert(
                "",
                END,
                values=(
                    producto.id,
                    producto.nombre,
                    f"${producto.precio:.2f}",
                    producto.unidad
                )
            )

    def _on_producto_selected(self, event):
        seleccion = self.tree_productos.selection()
        if not seleccion:
            return

        # Obtener valores del item seleccionado
        item = self.tree_productos.item(seleccion[0])
        valores = item["values"]

        # Actualizar campos del formulario
        self.entry_nombre.delete(0, END)
        self.entry_nombre.insert(0, valores[1])
        
        self.entry_precio.delete(0, END)
        self.entry_precio.insert(0, valores[2].replace("$", ""))
        
        self.combo_unidad.set(valores[3])

    def _agregar_producto(self):
        nombre = self.entry_nombre.get()
        precio = self.entry_precio.get()
        unidad = self.combo_unidad.get()

        success, mensaje, producto = self.controller.add_producto(nombre, precio, unidad)
        
        if success:
            ttk.dialogs.Messagebox.show_info(
                "Éxito",
                mensaje,
                parent=self.ventana
            )
            self._cargar_productos()
            self._limpiar_form_producto()
            # Actualizar combobox de ventas
            self.combo_producto["values"] = [p.nombre for p in self.controller.get_productos()]
        else:
            ttk.dialogs.Messagebox.show_error(
                "Error",
                mensaje,
                parent=self.ventana
            )

    def _modificar_producto(self):
        seleccion = self.tree_productos.selection()
        if not seleccion:
            ttk.dialogs.Messagebox.show_warning(
                "Advertencia",
                "Selecciona un producto para modificar",
                parent=self.ventana
            )
            return

        item = self.tree_productos.item(seleccion[0])
        id_producto = item["values"][0]
        nombre = self.entry_nombre.get()
        precio = self.entry_precio.get()
        unidad = self.combo_unidad.get()

        success, mensaje, producto = self.controller.update_producto(
            id_producto, nombre, precio, unidad
        )
        
        if success:
            ttk.dialogs.Messagebox.show_info(
                "Éxito",
                mensaje,
                parent=self.ventana
            )
            self._cargar_productos()
            self._limpiar_form_producto()
            # Actualizar combobox de ventas
            self.combo_producto["values"] = [p.nombre for p in self.controller.get_productos()]
        else:
            ttk.dialogs.Messagebox.show_error(
                "Error",
                mensaje,
                parent=self.ventana
            )

    def _eliminar_producto(self):
        seleccion = self.tree_productos.selection()
        if not seleccion:
            ttk.dialogs.Messagebox.show_warning(
                "Advertencia",
                "Selecciona un producto para eliminar",
                parent=self.ventana
            )
            return

        respuesta = ttk.dialogs.Messagebox.show_question(
            "Confirmar",
            "¿Estás seguro que deseas eliminar este producto?",
            parent=self.ventana
        )
        
        if respuesta == "Yes":
            item = self.tree_productos.item(seleccion[0])
            id_producto = item["values"][0]
            
            success, mensaje = self.controller.delete_producto(id_producto)
            
            if success:
                ttk.dialogs.Messagebox.show_info(
                    "Éxito",
                    mensaje,
                    parent=self.ventana
                )
                self._cargar_productos()
                self._limpiar_form_producto()
                # Actualizar combobox de ventas
                self.combo_producto["values"] = [p.nombre for p in self.controller.get_productos()]
            else:
                ttk.dialogs.Messagebox.show_error(
                    "Error",
                    mensaje,
                    parent=self.ventana
                )

    def _limpiar_form_producto(self):
        self.entry_nombre.delete(0, END)
        self.entry_precio.delete(0, END)
        self.combo_unidad.set("")
        if self.tree_productos.selection():
            self.tree_productos.selection_remove(self.tree_productos.selection())

    def _crear_botones_productos(self, frame):
        productos_frecuentes = self.controller.get_productos()[:8]  # Primeros 8 productos
        for i, producto in enumerate(productos_frecuentes):
            btn = ttk.Button(
                frame,
                text=f"{producto.nombre}",
                command=lambda p=producto: self._seleccionar_producto_rapido(p),
                bootstyle="primary-outline",
                width=15
            )
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)

    def _seleccionar_producto_rapido(self, producto):
        self.combo_producto.set(producto.nombre)
        self._actualizar_info_producto(None)
        self.entry_cantidad.focus()

    def _actualizar_info_producto(self, event):
        nombre = self.combo_producto.get()
        producto = self.controller.repository.get_producto_by_nombre(nombre)
        if producto:
            self.label_precio.config(text=f"Precio: ${producto.precio:.2f}")
            self.label_unidad.config(text=f"Unidad: {producto.unidad}")

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
            ttk.dialogs.Messagebox.show_error(
                "Cantidad inválida",
                "Por favor ingresa un número válido",
                parent=self.ventana
            )
            return

        success, mensaje, venta = self.controller.procesar_venta(nombre, cantidad)
        
        if not success:
            ttk.dialogs.Messagebox.show_error(
                "Error",
                mensaje,
                parent=self.ventana
            )
            return

        self.lista_ventas.insert(
            "",
            END,
            values=(
                venta.producto.nombre,
                f"{venta.cantidad} {venta.producto.unidad}",
                f"${venta.producto.precio:.2f}",
                f"${venta.total:.2f}"
            )
        )

        # Limpiar campos
        self.entry_cantidad.delete(0, END)
        self.combo_producto.set("")
        self.label_precio.config(text="Precio: -")
        self.label_unidad.config(text="Unidad: -")
        self._actualizar_total()

    def _eliminar_venta(self):
        seleccion = self.lista_ventas.selection()
        if not seleccion:
            ttk.dialogs.Messagebox.show_warning(
                "Advertencia",
                "Seleccioná un producto para eliminar",
                parent=self.ventana
            )
            return

        index = self.lista_ventas.index(seleccion[0])
        if self.controller.eliminar_venta(index):
            self.lista_ventas.delete(seleccion[0])
            self._actualizar_total()

    def _vaciar_ticket(self):
        respuesta = ttk.dialogs.Messagebox.show_question(
            "Confirmar",
            "¿Estás seguro que querés eliminar todo el ticket del día?",
            parent=self.ventana
        )
        if respuesta == "Yes":
            self.controller.vaciar_registro()
            for item in self.lista_ventas.get_children():
                self.lista_ventas.delete(item)
            self._actualizar_total()

    def _generar_venta(self):
        # Verificar si hay ventas en la lista
        if not self.lista_ventas.get_children():
            ttk.dialogs.Messagebox.show_warning(
                "No hay ventas",
                "Debe agregar al menos un producto para generar la venta",
                parent=self.ventana
            )
            return

        # Crear ventana personalizada para mostrar el total
        dialog = ttk.Toplevel(self.ventana)
        dialog.title("Total de la Venta")
        dialog.geometry("530x540")
        dialog.transient(self.ventana)
        dialog.grab_set()

        # Centrar la ventana
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - 530) // 2
        y = (screen_height - 540) // 2
        dialog.geometry(f"530x540+{x}+{y}")

        # Frame principal con padding
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        # Título
        ttk.Label(
            main_frame,
            text="TOTAL A COBRAR",
            font=("Helvetica", 16, "bold"),
            bootstyle="primary"
        ).pack(pady=(0, 20))

        # Monto total
        total_frame = ttk.Frame(main_frame)
        total_frame.pack(fill=X, pady=10)

        ttk.Label(
            total_frame,
            text="Monto Total:",
            font=("Helvetica", 14)
        ).pack(side=LEFT)

        total_actual = self.controller.total_actual
        ttk.Label(
            total_frame,
            text=f"${total_actual:.2f}",
            font=("Helvetica", 20, "bold"),
            bootstyle="success"
        ).pack(side=RIGHT)

        # Separador
        ttk.Separator(main_frame, orient=HORIZONTAL).pack(fill=X, pady=20)

        # Frame para el cálculo del vuelto
        vuelto_frame = ttk.LabelFrame(
            main_frame,
            text="Cálculo de Vuelto",
            padding=15,
            bootstyle="primary"
        )
        vuelto_frame.pack(fill=X, pady=10)

        # Monto recibido
        recibido_frame = ttk.Frame(vuelto_frame)
        recibido_frame.pack(fill=X, pady=5)

        ttk.Label(
            recibido_frame,
            text="Monto Recibido:",
            font=("Helvetica", 12)
        ).pack(side=LEFT)

        monto_recibido_var = ttk.StringVar()
        monto_recibido_entry = ttk.Entry(
            recibido_frame,
            textvariable=monto_recibido_var,
            font=("Helvetica", 12),
            width=15,
            bootstyle="primary"
        )
        monto_recibido_entry.pack(side=RIGHT)
        monto_recibido_entry.focus()

        # Vuelto
        vuelto_resultado_frame = ttk.Frame(vuelto_frame)
        vuelto_resultado_frame.pack(fill=X, pady=5)

        ttk.Label(
            vuelto_resultado_frame,
            text="Vuelto:",
            font=("Helvetica", 12)
        ).pack(side=LEFT)

        vuelto_label = ttk.Label(
            vuelto_resultado_frame,
            text="$0.00",
            font=("Helvetica", 16, "bold"),
            bootstyle="info"
        )
        vuelto_label.pack(side=RIGHT)

        def calcular_vuelto(*args):
            try:
                # Obtener el valor del monto recibido y convertirlo a float
                monto_texto = monto_recibido_var.get().strip()
                if not monto_texto:  # Si está vacío
                    vuelto_label.config(
                        text="$0.00",
                        bootstyle="info"
                    )
                    return

                # Reemplazar coma por punto para manejar ambos formatos
                monto_texto = monto_texto.replace(',', '.')
                # Convertir a Decimal en lugar de float
                from decimal import Decimal
                recibido = Decimal(monto_texto)
                
                # Redondear a 2 decimales para evitar problemas de precisión
                recibido = round(recibido, 2)
                vuelto = round(recibido - total_actual, 2)
                
                # Actualizar el label del vuelto
                if vuelto >= 0:
                    vuelto_label.config(
                        text=f"${float(vuelto):.2f}",
                        bootstyle="success"
                    )
                else:
                    vuelto_label.config(
                        text=f"Faltan ${abs(float(vuelto)):.2f}",
                        bootstyle="danger"
                    )
            except ValueError:
                vuelto_label.config(
                    text="Monto inválido",
                    bootstyle="danger"
                )

        # Vincular el cálculo al cambio del monto recibido
        monto_recibido_var.trace_add("write", calcular_vuelto)

        # Configurar el campo de monto recibido para aceptar solo números, punto y coma
        def validar_monto(P):
            if P == "": return True
            # Permitir solo números, un punto o una coma
            if P.count('.') <= 1 and P.count(',') <= 1:
                # Remover punto o coma para verificar si el resto son números
                P = P.replace('.', '').replace(',', '')
                return P.isdigit()
            return False

        vcmd = (dialog.register(validar_monto), '%P')
        monto_recibido_entry.config(validate='key', validatecommand=vcmd)

        # Formatear el monto al perder el foco
        def formatear_monto(event):
            try:
                monto_texto = monto_recibido_var.get().strip()
                if monto_texto:
                    # Reemplazar coma por punto
                    monto_texto = monto_texto.replace(',', '.')
                    # Convertir a Decimal y formatear
                    from decimal import Decimal
                    monto = Decimal(monto_texto)
                    monto_recibido_var.set(f"{float(monto):.2f}")
            except ValueError:
                pass

        monto_recibido_entry.bind('<FocusOut>', formatear_monto)

        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=X, pady=(20, 0))

        def finalizar_venta():
            try:
                recibido = float(monto_recibido_var.get() or 0)
                if recibido < total_actual:
                    ttk.dialogs.Messagebox.show_warning(
                        "Monto insuficiente",
                        "El monto recibido es menor al total a cobrar",
                        parent=dialog
                    )
                    return
                dialog.destroy()
                # Registrar la venta en el historial
                self.controller.registrar_venta_actual()
                # Limpiar la lista de ventas actual
                for item in self.lista_ventas.get_children():
                    self.lista_ventas.delete(item)
                self._actualizar_total()
                ttk.dialogs.Messagebox.show_info(
                    "Venta Finalizada",
                    "La venta ha sido registrada correctamente",
                    parent=self.ventana
                )
            except ValueError:
                ttk.dialogs.Messagebox.show_warning(
                    "Monto inválido",
                    "Por favor ingrese un monto válido",
                    parent=dialog
                )

        def cancelar():
            dialog.destroy()

        ttk.Button(
            btn_frame,
            text="Finalizar Venta",
            command=finalizar_venta,
            bootstyle="success",
            width=20
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Cancelar",
            command=cancelar,
            bootstyle="secondary",
            width=20
        ).pack(side=RIGHT, padx=5)

        # Hacer que la ventana sea modal
        dialog.wait_window()

    def _cerrar_caja(self):
        # Verificar si hay ventas en el historial
        if not self.controller.get_ventas_en_bd():
            ttk.dialogs.Messagebox.show_warning(
                "No hay ventas",
                "No hay ventas registradas para cerrar caja",
                parent=self.ventana
            )
            return

        # Crear diálogo para seleccionar turno
        dialog = ttk.Toplevel(self.ventana)
        dialog.title("Seleccionar Turno")
        dialog.geometry("400x200")
        dialog.transient(self.ventana)
        dialog.grab_set()

        # Frame para el diálogo
        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill=BOTH, expand=YES)

        ttk.Label(
            frame,
            text="Seleccione el turno:",
            font=("Helvetica", 12)
        ).pack(pady=10)

        # Frame para botones
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=X, pady=10)

        def seleccionar_turno(turno: str):
            dialog.destroy()
            success, mensaje = self.controller.cerrar_caja(turno)
            if success:
                ttk.dialogs.Messagebox.show_info(
                    "Cierre de Caja",
                    mensaje,
                    parent=self.ventana
                )
                # Limpiar la lista de ventas actual si hay algo
                for item in self.lista_ventas.get_children():
                    self.lista_ventas.delete(item)
                self._actualizar_total()
            else:
                ttk.dialogs.Messagebox.show_error(
                    "Error",
                    mensaje,
                    parent=self.ventana
                )

        ttk.Button(
            btn_frame,
            text="Mañana",
            command=lambda: seleccionar_turno("mañana"),
            bootstyle="primary",
            width=15
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Tarde",
            command=lambda: seleccionar_turno("tarde"),
            bootstyle="primary",
            width=15
        ).pack(side=LEFT, padx=5)

    def _cargar_ventas_bd(self):
        # Limpiar tree
        for item in self.tree_ventas_bd.get_children():
            self.tree_ventas_bd.delete(item)
        # Cargar ventas desde el controlador
        ventas = self.controller.get_ventas_en_bd()
        for venta in ventas:
            self.tree_ventas_bd.insert(
                "",
                END,
                values=(
                    venta.id,
                    venta.producto.nombre,
                    venta.cantidad,
                    venta.fecha
                )
            )

    def _eliminar_venta_bd(self):
        seleccion = self.tree_ventas_bd.selection()
        if not seleccion:
            ttk.dialogs.Messagebox.show_warning(
                "Advertencia",
                "Selecciona una venta para eliminar",
                parent=self.ventana
            )
            return
        item = self.tree_ventas_bd.item(seleccion[0])
        venta_id = item["values"][0]
        respuesta = ttk.dialogs.Messagebox.show_question(
            "Confirmar",
            "¿Estás seguro que deseas eliminar esta venta?",
            parent=self.ventana
        )
        if respuesta == "Yes":
            success, mensaje = self.controller.delete_venta_en_bd(venta_id)
            if success:
                ttk.dialogs.Messagebox.show_info(
                    "Éxito",
                    mensaje,
                    parent=self.ventana
                )
                self._cargar_ventas_bd()
            else:
                ttk.dialogs.Messagebox.show_error(
                    "Error",
                    mensaje,
                    parent=self.ventana
                )

    def _modificar_venta_bd(self):
        seleccion = self.tree_ventas_bd.selection()
        if not seleccion:
            ttk.dialogs.Messagebox.show_warning(
                "Advertencia",
                "Selecciona una venta para modificar",
                parent=self.ventana
            )
            return
        item = self.tree_ventas_bd.item(seleccion[0])
        venta_id = item["values"][0]
        producto_nombre = item["values"][1]
        cantidad = item["values"][2]
        fecha = item["values"][3]

        # Ventana de edición
        edit_win = ttk.Toplevel(self.ventana)
        edit_win.title("Modificar Venta")
        edit_win.geometry("400x300")
        edit_win.transient(self.ventana)
        edit_win.grab_set()

        frame = ttk.Frame(edit_win, padding=20)
        frame.pack(fill=BOTH, expand=YES)

        # Producto
        ttk.Label(frame, text="Producto:").pack(anchor=W)
        productos = self.controller.get_productos()
        producto_nombres = [p.nombre for p in productos]
        producto_var = ttk.StringVar(value=producto_nombre)
        combo_producto = ttk.Combobox(frame, values=producto_nombres, textvariable=producto_var, state="readonly")
        combo_producto.pack(fill=X, pady=5)

        # Cantidad
        ttk.Label(frame, text="Cantidad:").pack(anchor=W)
        cantidad_var = ttk.StringVar(value=str(cantidad))
        entry_cantidad = ttk.Entry(frame, textvariable=cantidad_var)
        entry_cantidad.pack(fill=X, pady=5)

        # Fecha
        ttk.Label(frame, text="Fecha (YYYY-MM-DD HH:MM:SS):").pack(anchor=W)
        fecha_var = ttk.StringVar(value=fecha)
        entry_fecha = ttk.Entry(frame, textvariable=fecha_var)
        entry_fecha.pack(fill=X, pady=5)

        def guardar_cambios():
            nuevo_producto_nombre = producto_var.get()
            nuevo_producto = next((p for p in productos if p.nombre == nuevo_producto_nombre), None)
            if not nuevo_producto:
                ttk.dialogs.Messagebox.show_error(
                    "Error",
                    "Producto inválido",
                    parent=edit_win
                )
                return
            try:
                nueva_cantidad = float(cantidad_var.get())
            except ValueError:
                ttk.dialogs.Messagebox.show_error(
                    "Error",
                    "Cantidad inválida",
                    parent=edit_win
                )
                return
            nueva_fecha = fecha_var.get()
            success, mensaje = self.controller.update_venta_en_bd(venta_id, nuevo_producto.id, nueva_cantidad, nueva_fecha)
            if success:
                ttk.dialogs.Messagebox.show_info(
                    "Éxito",
                    mensaje,
                    parent=edit_win
                )
                edit_win.destroy()
                self._cargar_ventas_bd()
            else:
                ttk.dialogs.Messagebox.show_error(
                    "Error",
                    mensaje,
                    parent=edit_win
                )

        ttk.Button(frame, text="Guardar Cambios", command=guardar_cambios, bootstyle="success").pack(pady=10)
        ttk.Button(frame, text="Cancelar", command=edit_win.destroy, bootstyle="secondary").pack()

    def run(self):
        self.ventana.mainloop() 