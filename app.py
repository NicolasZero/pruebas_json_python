# Librerias
from pathlib import Path
import json
import os
import requests

# Definicion de constantes
class Constantes:
    """
    Definicion de constantes para el programa.
    """
    RUTA_ARCHIVO: str = Path(__file__).parent / "datos" / "zonas_caracas.json"
    URL_API: str = "https://api.open-meteo.com/v1/forecast"
    WEATHER_CODE = {
        0: "Despejado",
        1: "Mayormente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna moderada",
        55: "Llovizna intensa",
        56: "Llovizna ligera helada",
        57: "Llovizna intensa helada",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia intensa",
        66: "Lluvia ligera helada",
        67: "Lluvia intensa helada",
        71: "Nieve ligera",
        73: "Nieve moderada",
        75: "Nieve intensa",
        77: "Granos de hielo",
        80: "Chubascos de lluvia ligera",
        81: "Chubascos de lluvia moderada",
        82: "Chubascos de lluvia intensa",
        83: "Chubascos de nieve ligera",
        84: "Chubascos de nieve moderada",
        85: "Chubascos de nieve intensa",
        86: "Chubascos de aguanieve",
        95: "Tormenta eléctrica",
        96: "Tormenta eléctrica con granizo ligero",
        99: "Tormenta eléctrica con granizo intenso"
    }

# Se separaron las clases para respetar la poo

# PAra la lista de objetos
class Localidad:
    """
    Localidad: nombre, municipio y coordenadas (longitud y latitud).
    """
    def __init__(self, nombre, municipio, longitud, latitud):
        self.nombre = nombre
        self.municipio = municipio
        self.longitud = longitud
        self.latitud = latitud

# Clase separada para leer el json
class LeerJSON:
    """
    Gestiona la lectura del archivo JSON.
    """
    def __init__(self):
        self.ruta_archivo = Constantes.RUTA_ARCHIVO

    def cargar_datos(self):
        localidades = []
        if not self.ruta_archivo.exists():
            return localidades

        with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        
        for municipio in datos:
            for localidad in datos[municipio]:
                localidades.append(Localidad(localidad['localidad'], municipio, localidad['longitud'], localidad['latitud']))
        
        return localidades

# separado de main para las estadisticas
class Estadisticas:
    """
    Se encarga exclusivamente de calcular y almacenar las estadisticas sobre las localidades.
    """
    def __init__(self, lista_localidades):
        self.lista_localidades = lista_localidades
        self.total_municipios = len(set(loc.municipio for loc in lista_localidades))
        self.total_localidades = len(lista_localidades)
        self.con_coordenadas = sum(1 for loc in lista_localidades if loc.longitud is not None and loc.latitud is not None)
        self.sin_coordenadas = self.total_localidades - self.con_coordenadas # Es mas facil si se resta
        self.porc_con_coordenadas = round((self.con_coordenadas / self.total_localidades) * 100, 2) if self.total_localidades > 0 else 0.0
        self.porc_sin_coordenadas = round((self.sin_coordenadas / self.total_localidades) * 100, 2) if self.total_localidades > 0 else 0.0

    def mostrar_estadisticas(self):
        print(f"Total de municipios: {self.total_municipios}")
        print(f"Total de localidades: {self.total_localidades}")
        print(f"Localidades con coordenadas: {self.con_coordenadas} ({self.porc_con_coordenadas}%)")
        print(f"Localidades sin coordenadas: {self.sin_coordenadas} ({self.porc_sin_coordenadas}%)")

# Clase para obtener los datos del clima
class Clima:
    """
    Gestiona la obtención de datos del clima de una localidad.
    """
    def __init__(self):
        self._url_api = Constantes.URL_API

    def obtener_clima(self, localidad):
        """
        Obtiene los datos del clima para una localidad específica.
        :param localidad: Localidad para la cual obtener los datos del clima.
        :return: Diccionario con los datos del clima.
        """
        if localidad.latitud is None or localidad.longitud is None:
            return "No se pueden obtener los datos del clima para esta localidad porque no tiene coordenadas."
        
        # Try para manejar el error con la api
        try:
            url = f"{self._url_api}?latitude={localidad.latitud}&longitude={localidad.longitud}&current=weather_code"
            response = requests.get(url)
            datos = response.json()
            clima = Constantes.WEATHER_CODE[datos["current"]["weather_code"]] 
            return f"El clima en {localidad.nombre} es: {clima}"
        except Exception:
            return "Error al obtener los datos del clima"

#  Para gestionar la interfaz
class Interfaz:
    """
    Maneja toda la interacción con el usuario a través de la consola.
    """
    def limpiar_pantalla(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def mostrar_menu(self):
        print("\n-----> MENÚ PRINCIPAL <-----")
        print("1.- Seleccionar un municipio y su localidad")
        print("2.- Ver estadisticas de los municipios y localidades")
        print("3.- Buscar una localidad")
        print("0.- Salir")
        return input("\nElige una opcion: ")

    def esperar_enter(self):
        input("\nPresiona Enter para continuar...")

    def seleccionar_municipio(self, lista_municipios, lista_localidades):
        for i, municipio in enumerate(lista_municipios):
            print(f"{i + 1}. {municipio}")
        
        eleccion = input("\nSeleccione un municipio: ")
        if not eleccion.isdigit():
            print("Error: Por favor, ingrese un número.")
            return None
        eleccion = int(eleccion)
        if eleccion < 1 or eleccion > len(lista_municipios):
            print("Error: El número seleccionado no es válido.")
            return None
        
        municipio_seleccionado = lista_municipios[eleccion - 1]
        
        # Filtrar e imprimir localidades del municipio seleccionado (que tengan coordenadas)
        for i, localidad in enumerate(lista_localidades):
            if localidad.municipio == municipio_seleccionado:
                if localidad.latitud is not None and localidad.longitud is not None:
                    print(f"{i + 1}. {localidad.nombre}")
                    
        eleccion2 = input("\nSeleccione una localidad: ")
        if not eleccion2.isdigit():
            print("Error: Por favor, ingrese un número.")
            return None
        eleccion2 = int(eleccion2)
        if eleccion2 < 1 or eleccion2 > len(lista_localidades):
            print("Error: El número seleccionado no es válido.")
            return None
            
        return lista_localidades[eleccion2 - 1]

    def mostrar_estadisticas(self, estadisticas):
        estadisticas.mostrar_estadisticas()

    def buscar_localidad(self, lista_localidades):
        print("\n-----> BUSCAR LOCALIDAD <-----")
        nombre_busqueda = input("Ingrese el nombre de la localidad: ").strip().lower()
        encontradas = []

        for localidad in lista_localidades:
            if nombre_busqueda in localidad.nombre.lower():
                encontradas.append(localidad)
                print(f"{len(encontradas)}. {localidad.nombre} - {localidad.municipio}")

        if len(encontradas) == 0:
            print("Localidad no encontrada.")
            return None
        
        print(f"\nSe encontraron {len(encontradas)} localidades.")
        eleccion = input("Ingrese el número de la localidad que desea seleccionar: ")
        if not eleccion.isdigit():
            print("Error: Por favor, ingrese un número.")
            return None
        eleccion = int(eleccion)
        if eleccion < 1 or eleccion > len(encontradas):
            print("Error: El número seleccionado no es válido.")
            return None
            
        return encontradas[eleccion - 1]

#  Para la aplicacion principal
class Aplicacion:
    """
    Controlador u orquestador de la aplicación.
    Se encarga de coordinar la vista, el repositorio y el servicio de clima.
    """
    def __init__(self):
        self.archivo = LeerJSON()
        self.interfaz = Interfaz()
        self.servicio_clima = Clima()
        self.localidades = []
        self.municipios = []
        self.activo = True # Para el menu

    def iniciar(self):
        # 0. LIMPIAR PANTALLA
        self.interfaz.limpiar_pantalla()
        # 1. Cargar datos
        self.localidades = self.archivo.cargar_datos()
        # Se cambio como se genera la lista de municipios
        vistos = set()
        self.municipios = []
        for loc in self.localidades:
            if loc.municipio not in vistos:
                vistos.add(loc.municipio)
                self.municipios.append(loc.municipio)

        # 2. Mostrar estadísticas iniciales
        stats = Estadisticas(self.localidades)
        stats.mostrar_estadisticas()

        # 3. Ciclo del menú principal
        while self.activo:
            opcion = self.interfaz.mostrar_menu()
            
            if opcion == "1":
                self.interfaz.limpiar_pantalla()
                localidad = self.interfaz.seleccionar_municipio(self.municipios, self.localidades)
                if localidad:
                    print("\n-----> DATOS DEL CLIMA <-----\n")
                    clima_info = self.servicio_clima.obtener_clima(localidad)
                    print(clima_info)
            elif opcion == "2":
                self.interfaz.limpiar_pantalla()
                stats = Estadisticas(self.localidades)
                self.interfaz.mostrar_estadisticas(stats)
            elif opcion == "3":
                self.interfaz.limpiar_pantalla()
                localidad = self.interfaz.buscar_localidad(self.localidades)
                if localidad:
                    print("\n-----> DATOS DEL CLIMA <-----")
                    clima_info = self.servicio_clima.obtener_clima(localidad)
                    print(clima_info)
            elif opcion == "0":
                self.interfaz.limpiar_pantalla()
                self.activo = False
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida. Intenta de nuevo.")
            
            self.interfaz.esperar_enter()
            self.interfaz.limpiar_pantalla()

# Ejecutar el aplicacion
app = Aplicacion()
app.iniciar()