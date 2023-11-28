import ttkbootstrap as tkk
import pandas as pd
from ttkbootstrap.constants import *
from tkinter import font
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA, COLOR_CUERPO_PRINCIPAL
from ttkbootstrap.tableview import Tableview
import util.util_ventana as util_ventana
import util.util_img as util_img
import util.manipulacion as extract

class FormularioMaestroDesign(tkk.Window):

    def __init__(self):
        super().__init__(themename="superhero")
        self.columnas = ['pH bocatoma', 'pH salida', 'Turbiedad', 'Cloro residual', 'Macro 1', 'Macro 2', 'Macro 3', 'Macro 4',
                         'Sensor de nivel', 'Q T -entrada', 'Q T -salida', 'V horario E',
                         'V horario S', 'V regulacion', 'V real']
        self.logo = util_img.leer_imagen("imagenes/logo.png", (560, 136))
        self.perfil = util_img.leer_imagen("imagenes/logo2.png", (100, 100))
        self.menu = util_img.leer_imagen("imagenes\menu.ico", (32, 32))
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()

    def config_window(self):
        self.title('Graficadora')
        self.iconbitmap("imagenes/icono.ico")
        w, h = 1024, 600
        util_ventana.centrar_ventana(self, w, h)

    def table(self):
        d = extract.cargar_datos()
        datos = [tuple(x) for x in d.values]
        columnas = [{'text': col} for col in d.columns]
        self.tabla = Tableview(self.cuerpo_principal, coldata=columnas, rowdata=datos, paginated=True, searchable=False, pagesize=100, autofit=TRUE)
        self.tabla.pack(side=tkk.TOP, fill=BOTH, expand=YES, pady=10, padx=10)

    def filtro_calendario(self, event):
        fecha = self.calendar.entry.get()
        print(fecha)

    def crear_radiobotones(self, master, lista_variables, estilo):
        self.lista_radioBotones = []
        i = 0
        for variable in lista_variables:
            self.lista_radioBotones.append(tkk.Radiobutton(master, text=variable, bootstyle=estilo))
            i = i + 1
        return self.lista_radioBotones
    def paneles(self):

        self.barra_superior = tkk.Frame(
            self, height=50, bootstyle="dark")
        self.barra_superior.pack(side=tkk.TOP, fill='both')

        self.menu_lateral = tkk.Frame(
            self, width=150, bootstyle='dark')
        self.menu_lateral.pack(side=tkk.LEFT, fill='both', expand=False)

        self.cuerpo_principal = tkk.Frame(
            self, width=150, bootstyle="light")
        self.cuerpo_principal.pack(side=tkk.RIGHT, fill='both', expand=True)

    def controles_barra_superior(self):

        font_awesome = font.Font(family='FontAwesome', size=12)

        self.labelTitulo = tkk.Label(self.barra_superior, text="Graficadora de variables", font=(
            "Roboto", 15), padding=20, width=20)
        self.labelTitulo.config(foreground="#fff")
        self.labelTitulo.pack(side=tkk.LEFT)

        self.button_menu_lateral = tkk.Menubutton(self.barra_superior, text="\uf0c9", image=self.menu, bootstyle="dark")
        self.button_menu_lateral.pack(side=tkk.LEFT)
        self.desplegable_menu = tkk.Menu(self.button_menu_lateral)
        self.options = tkk.StringVar()
        self.desplegable_menu.add_radiobutton(label='Abrir', command=self.table)
        #self.desplegable_menu.add_radiobutton(label='Exportar', value=self.options)
        self.button_menu_lateral['menu'] = self.desplegable_menu

        self.labelTitulo = tkk.Label(
            self.barra_superior, text="cristian.quinterom94@hotmail.com", font=(
                "Roboto", 10), padding=10, width=30)
        self.labelTitulo.config(foreground="#fff")
        self.labelTitulo.pack(side=tkk.RIGHT)

    def controles_menu_lateral(self):
        ancho_menu=20
        alto_menu=2
        font_awesome = font.Font(family='FontAwesome', size=15)

        self.labelPerfil = tkk.Label(
            self.menu_lateral, image=self.perfil)
        self.labelPerfil.pack(side=tkk.TOP, pady=10)

        self.calendar = tkk.DateEntry(self.menu_lateral, dateformat='%Y-%m-%d')
        self.calendar.bind('<Button-1>', self.filtro_calendario)
        self.calendar.pack(side=tkk.TOP)

        #self.filtro_columnas = tkk.Combobox(self.menu_lateral, values=['pH bocatoma', 'pH salida', 'Turbiedad', 'Cloro residual', 'Macro 1', 'Macro 2', 'Macro 3', 'Macro 4',
        #               'Sensor de nivel', 'Q T -entrada', 'Q T -salida', 'V horario E', 'V horario S', 'V regulacion', 'V real'])
        #self.filtro_columnas.pack(side=tkk.TOP, pady=10, fill=BOTH)


        lista_botones = self.crear_radiobotones(self.menu_lateral, self.columnas, "toolbutton")

        for boton in lista_botones:
            boton.pack(side=tkk.TOP, pady=1, fill=BOTH)