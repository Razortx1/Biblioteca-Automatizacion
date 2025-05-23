"""
    **Modulo historia_libros**\n
    Es el modulo que se encarga de la parte visual con la cual el usuario
    podra revisar el historial de los libros que haya dentro del sistema\n

    **Importaciones del modulo**\n
    PyQt5.QtWidgets ----> Usado principalmente para obtener los widgets que serán
                            usados durante la vista de los diversos libros\n
    PyQt5.QtCore ----> Usado para obtener, ya sean las señales, o algunas
                        configuraciones adicionales para los widgets\n
    PyQt.QtGui -----> Usado para cambiar los colores de la ultima columna de la tabla

    modulo session -----> Usado para poder obtener todos los estados del prestamo y los libros que 
                            pertenezcan al prestamo

"""

from PyQt5.QtWidgets import (QWidget, QPushButton, QTableWidgetItem, QTableWidget,
                             QAbstractItemView, QVBoxLayout, QHeaderView, QHBoxLayout,
                             QMessageBox, QComboBox, QLineEdit, QLabel)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor

from connection.session import (select_libros_available, select_estado_libro_all)
from .actualizar_ui.actualizar_libros import ActualizarLibros

class HistorialLibros(QWidget):
    """
    **Clase HistorialLibros**\n
    Permite el poder observar los distintos libros que se posee en la biblioteca,
    esto a traves de filtros y paginaciones
    """
    volver_principal = pyqtSignal()
    ir_prestamo_libro = pyqtSignal(str, str, str)
    pasar_datos = pyqtSignal(str, str, str)

    def __init__(self, parent = None):
        """
        **Funcion __ init __**\n
        Permite la carga de todos y cada uno de los widgets que se utilizaran durante el ciclo
        de vida de esta ventana
        """
        super().__init__(parent)

        # Lista para filtros
        self.filtros_actuales = {
        "nombre_": "",
        "autor_": "",
        "no_editorial": "",
        "estado": "",
        "biblioteca_": "",
        "estanteria_": ""
        }

        self.w = None
        # Layout principal
        main_layout = QVBoxLayout()

        # Layout para filtrado
        filtro_layout = QHBoxLayout()

        pagination_layout = QHBoxLayout()

        # PushButtons para filtrado de tabla
        self.filtrar = QPushButton("Aplicar Filtro(s)")
        self.quitar_filtro = QPushButton("Quitar Filtro(s)")

        # Combobox para filtrado de tabla
        self.estado_filtro = QComboBox()

        # PushButtons para paginacion
        self.anterior = QPushButton("Pagina Anterior")
        self.anterior.setDisabled(True)
        self.siguiente = QPushButton("Pagina Siguiente")

        #Label para paginacion
        self.pagina = QLabel()
        self.pagina.setAlignment(Qt.AlignCenter)

        # LineEdit para filtrado de tabla
        self.nombre_filtro = QLineEdit()
        self.nombre_filtro.setPlaceholderText("Nombre del libro")

        self.sector_biblioteca = QLineEdit()
        self.sector_biblioteca.setPlaceholderText("Sector Biblioteca")

        self.sector_estanteria = QLineEdit()
        self.sector_estanteria.setPlaceholderText("Sector Estanteria")

        self.editorial = QLineEdit()
        self.editorial.setPlaceholderText("Editoral")

        self.autor_libro = QLineEdit()
        self.autor_libro.setPlaceholderText("Autor")

        # Crear la tabla de libros
        self.tabla_libros = QTableWidget()
        self.tabla_libros.setColumnCount(8)
        headers = ["Nombre Libro", "Autor", "Editorial", "Fecha Entrada a Biblioteca","Area de Biblioteca", 
                   "Sector Estanteria" , "Stock de Libros", "Estado del Libro"]
        self.tabla_libros.setMinimumHeight(300)
        self.tabla_libros.setMaximumHeight(400)
        
        # Asignar encabezados de las columnas
        for i, header in enumerate(headers):
            item = QTableWidgetItem(header)
            self.tabla_libros.setHorizontalHeaderItem(i, item)

        # Hacer que las columnas se ajusten al tamaño de la ventana
        header = self.tabla_libros.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Crear los botones
        self.cambiar_estado = QPushButton("Cambiar Estado Libro")
        self.volver_inicio = QPushButton("Volver al Menu Principal")
        self.agregar_prestamo = QPushButton("Agregar prestamo del libro")

        # Agregar los widgets al layout principal
        button_layout = QHBoxLayout()
        
        button_layout.addWidget(self.cambiar_estado)
        button_layout.addWidget(self.volver_inicio)

        filtro_layout.addWidget(self.nombre_filtro)
        filtro_layout.addWidget(self.autor_libro)
        filtro_layout.addWidget(self.editorial)
        filtro_layout.addWidget(self.sector_biblioteca)
        filtro_layout.addWidget(self.sector_estanteria)
        filtro_layout.addWidget(self.estado_filtro)
        filtro_layout.addWidget(self.filtrar)
        filtro_layout.addWidget(self.quitar_filtro)

        pagination_layout.addWidget(self.anterior)
        pagination_layout.addWidget(self.pagina)
        pagination_layout.addWidget(self.siguiente)

        main_layout.addLayout(filtro_layout)
        main_layout.addWidget(self.tabla_libros)
        main_layout.addLayout(pagination_layout)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.agregar_prestamo)
        main_layout.addLayout(button_layout)
        self.number = 0

        self.pagina.setText("Pagina 1")

        # Paginaciones
        self.current_page = 0
        self.page_size = 7

        # Seleccion de datos desde la tabla
        self.tabla_libros.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_libros.setSelectionMode(QAbstractItemView.SingleSelection)

        # Agregar espaciadores si es necesario (opcional)
        main_layout.addStretch(1)

        # Establecer el layout principal
        self.setLayout(main_layout)

        # Conectar los botones con las funciones
        self.cambiar_estado.clicked.connect(self.actualizar_estado)
        self.volver_inicio.clicked.connect(self.volver_principal.emit)
        self.agregar_prestamo.clicked.connect(self.prestamo_ir)
        self.filtrar.clicked.connect(self.aplicar_filtros)
        self.quitar_filtro.clicked.connect(self.vaciar_filtrado)

        self.anterior.clicked.connect(self.anterior_funcion)
        self.siguiente.clicked.connect(self.siguiente_funcion)

    # Rellenado del combobox
    def rellenar_combobox(self):
        """
        **Funcion rellenar_combobox**\n
        Permite el poder rellenar los combobox que se encuentran como filtros
        """
        self.estado_filtro.clear()
        self.estado_filtro.addItem("Selecciona un estado")
        estado = select_estado_libro_all()
        for es in estado:
            self.estado_filtro.addItem(es[0].estado_libro)

    # Funcion Boton siguiente-anterior
    def anterior_funcion(self):
        """
        **Funcion anterior_funcion**\n
        Permite poder manejar las paginaciones con los respectivos botones,
        ademas del label utilizado para mostrar la pagina actual
        Se usa normalmente para disminuir la cantidad de paginas
        """
        if self.current_page > 0:
                self.current_page -=1
                self.pagina.setText(f"Pagina {self.current_page +1}")
                self.rellenar_tabla(**self.filtros_actuales)
    def siguiente_funcion(self):
        """
        **Funcion siguiente_funcion**\n
        Permite poder manejar las paginaciones con los respectivos botones,
        ademas del label utilizado para mostrar la pagina actual.\n
        Se usa normalmente para incrementar la cantidad de paginas
        """
        self.current_page+=1
        self.pagina.setText(f"Pagina {self.current_page +1}")
        self.anterior.setDisabled(False)
        self.rellenar_tabla(**self.filtros_actuales)


    def rellenar_tabla(self, nombre_=None, autor_=None,
                       no_editorial=None,estado=None, biblioteca_=None, estanteria_=None ):
        """
        **Funcion rellenar_tabla**\n
        Es la encargada de traer todos los libros que actualmente hay en biblioteca, sin tomar en cuenta los que estan
        prestamos, y que una vez tenga los datos, estos los carga en la tabla, ademas funciona tambien en base a 
        filtros.

        **Parametros**\n
        - nombre: str | None\n
        - autor: str | None\n
        - no_editorial: str | None\n
        - estado: str | None\n
        - biblioteca: str | None\n
        - estanteria: str | None\n
        """
        offset = self.current_page * self.page_size
        libros = list(select_libros_available(nombre=nombre_,autor= autor_,Editorial=no_editorial, Estado_=estado,
                                         SectorBiblio=biblioteca_, SectorEstanteria=estanteria_ ,offset=offset, limit=self.page_size+1))
        if len(libros) > self.page_size:
            self.siguiente.setDisabled(False)
            libros = libros[:self.page_size]
        else:
            self.siguiente.setDisabled(True)
        if self.current_page == 0:
            self.anterior.setDisabled(True)
        else:
            self.anterior.setDisabled(False)
        self.tabla(libros)
        


    def vaciar_filtrado(self):
        """
        **Funcion vaciar_filtrado**\n
        Es la encargada de devolver todos los valores de los filtros a vacio, o en caso de ser un combobox,
        se regresa a su indice 0, el cual esta establecido como 'Selecciona...'
        """
        self.estado_filtro.setCurrentIndex(0)
        self.sector_biblioteca.clear()
        self.sector_estanteria.clear()
        self.editorial.clear()
        self.nombre_filtro.clear()
        self.autor_libro.clear()
        self.filtros_actuales = {
        "nombre_": "",
        "autor_": "",
        "no_editorial": "",
        "estado": "",
        "biblioteca_": "",
        "estanteria_": ""
        }
        self.rellenar_tabla(**self.filtros_actuales)
        self.current_page = 0
        self.pagina.setText("Pagina 1")

    def aplicar_filtros(self):
        """
        **Funcion aplicar_filtros**\n
        Se encarga de aplicar los filtros que el usuario propuso a traves de la barra de filtros para luego,
        rellenar la tabla con dichos datos
        """
        biblioteca = self.sector_biblioteca.text()
        estanteria = self.sector_estanteria.text()
        no_editorial = self.editorial.text()
        autor = self.autor_libro.text()
        nombre = self.nombre_filtro.text()
        estado = ""
        self.current_page = 0
        self.pagina.setText("Pagina 1")
        if self.estado_filtro.currentText() != "Selecciona un estado":
            estado = self.estado_filtro.currentText()
        elif estado == "Selecciona un estado":
            return
        self.filtros_actuales = {
        "nombre_": nombre,
        "autor_": autor,
        "no_editorial": no_editorial,
        "estado": estado,
        "biblioteca_": biblioteca,
        "estanteria_": estanteria
        }
        self.rellenar_tabla(nombre_=nombre, autor_=autor, no_editorial=no_editorial,
                                     estado=estado, biblioteca_=biblioteca, estanteria_=estanteria)
        
    def prestamo_ir(self):
        """
        **Funcion prestamo_ir**\n
        Es la encargada de poder obtener los datos que fueron seleccionados desde la tabla para mandar dichos datos a traves de emisiones
        de señales, estos datos son:\n

        **Datos enviados como emision de señal**\n
        - nombre: str\n
        - autor: str\n
        - editorial: str
        """
        selected_rows = self.tabla_libros.selectionModel().selectedRows()
        if not selected_rows:
            msg = QMessageBox()
            msg.setWindowTitle("Seleccion Invalida")
            msg.setText("Por favor, selecciona un libro antes de continuar")
            msg.setIcon(QMessageBox.Information)
            msg.exec()
            return
        for row in selected_rows:
            nombre = self.tabla_libros.item(row.row(), 0).text()
            autor = self.tabla_libros.item(row.row(), 1).text()
            editorial = self.tabla_libros.item(row.row(), 2).text()
        self.ir_prestamo_libro.emit(nombre, autor, editorial)

    def tabla(self, libros):
        """
        **Funcion tabla**\n
        Se encarga de poder rellenar la tabla con datos, ademas de asignarles los colores correspondientes a los estados
        de la tabla\n

        **Parametros**\n
        - libros: List[Libro]
        """
        self.tabla_libros.setRowCount(0)
        mal_estado = QColor("#ffd62e")  # Mal estado
        buen_estado = QColor("#b2f7b2")  # Buen estado
        dado_baja = QColor("#ff6b6b")  # Dado de baja
        estado_regular = QColor("#ffe066")  # Estado regular

        if libros:
            for li in libros:
                row_position = self.tabla_libros.rowCount()
                self.tabla_libros.insertRow(row_position)

                # Insertar los datos del libro
                self.tabla_libros.setItem(row_position, 0, QTableWidgetItem(li.nombre_libro))
                self.tabla_libros.setItem(row_position, 1, QTableWidgetItem(li.autor))
                self.tabla_libros.setItem(row_position, 2, QTableWidgetItem(li.editorial))
                self.tabla_libros.setItem(row_position, 3, QTableWidgetItem(str(li.fecha_entrada)))
                self.tabla_libros.setItem(row_position, 4, QTableWidgetItem(li.sector_biblioteca))
                self.tabla_libros.setItem(row_position, 5, QTableWidgetItem(li.sector_estanteria))
                self.tabla_libros.setItem(row_position, 6, QTableWidgetItem(str(li.stock)))
                self.tabla_libros.setItem(row_position, 7, QTableWidgetItem(li.estado_libro))

                # Asignar colores dependiendo del estado
                estado_libro = self.tabla_libros.item(row_position, 7).text()

                if estado_libro == "Buen Estado":
                    self.tabla_libros.item(row_position, 7).setBackground(buen_estado)
                elif estado_libro == "Mal Estado":
                    self.tabla_libros.item(row_position, 7).setBackground(mal_estado)
                elif estado_libro == "Estado Regular":
                    self.tabla_libros.item(row_position, 7).setBackground(estado_regular)
                elif estado_libro == "Dado de Baja":
                    self.tabla_libros.item(row_position, 7).setBackground(dado_baja)
        else:
            return

    def actualizar_estado(self):
        """
        **Funcion actualizar_estado**\n
        Es la encargada de llamar a la ventana para actualizar los datos de los libros.\n
        Esta envia los datos a traves de señales y una vez enviado los datos, llama a la ventana.\n
        """
        selected_row = self.tabla_libros.selectionModel().selectedRows()
        if not selected_row:
            msg = QMessageBox()
            msg.setWindowTitle("Seleccion Invalida")
            msg.setText("Por favor, selecciona un libro antes de continuar")
            msg.setIcon(QMessageBox.Information)
            msg.exec()
            return
        
        for row in selected_row:
            nombre = self.tabla_libros.item(row.row(), 0).text()
            autor = self.tabla_libros.item(row.row(), 1).text()
            editorial = self.tabla_libros.item(row.row(), 2).text()
        if self.w is None:
            self.w = ActualizarLibros()
            self.w.actualizar_datos.connect(self.rellenar_tabla)
            self.pasar_datos.connect(self.w.traer_datos)
            self.pasar_datos.emit(nombre, autor, editorial)
            self.w.show()
            self.w.cerrar_ventana.connect(self.cerrar_ventana)

    def cerrar_ventana(self):
        """
        **Funcion cerrar_ventana**\n
        Es la encargada para poder comprobar si, existe o no existe una instancia de la ventana para
        actualizar los libros, y en caso que si haya una, esta se sobreescribe por None, esto con el
        fin de poder abrir nuevamente la ventana sin necesidad de cerrar la aplicacion donde ademas,
        una vez cerrada la ventana, se vuelven a cargar los datos de la tabla, esto para mantener actualizado
        lo mas posible los datos
        """
        if self.w is not None:
            self.w = None
            self.rellenar_tabla()
