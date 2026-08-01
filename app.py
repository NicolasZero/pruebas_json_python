# Para poder leer archivos json
import json
from pathlib import Path

# CONSTANTE
RUTA_ARCHIVO_PRINCIPAL = Path(__file__).parent / "datos"

# Definir las clases
class Main:
    """
    Esta clase se encarga de la carga de datos de un archivo json, el manejo de los datos y la ejecucion del programa.
    """
    def __init__(self, archivo):
        """
        Inicializa la clase.
        :param archivo: Ruta del archivo json a cargar.
        """
        self.archivo = archivo
        self.lista_municipios = []
        self.cantidad_municipios = 0
        self.cant_loc_sin_coordenadas = 0
        self.cant_loc_con_coordenadas = 0
        self.porc_loc_sin_coordenadas = 0
        self.porc_loc_con_coordenadas = 0

    def cargar_datos(self):
        """
        Carga los datos del archivo json y los guarda en la lista de municipios.
        Genera las estadisticas de los datos cargados.
        """
        with open(RUTA_ARCHIVO_PRINCIPAL / self.archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        for municipio in datos:
            for localidad in datos[municipio]:
                self.lista_municipios.append(Municipio(municipio, localidad['longitud'], localidad['latitud'], localidad['localidad']))
                if localidad['longitud'] is None or localidad['latitud'] is None:
                    self.cant_loc_sin_coordenadas += 1
                else:
                    self.cant_loc_con_coordenadas += 1
            self.cantidad_municipios += 1
        self.porc_loc_sin_coordenadas = round((self.cant_loc_sin_coordenadas / (self.cant_loc_con_coordenadas + self.cant_loc_sin_coordenadas)) * 100, 2)
        self.porc_loc_con_coordenadas = round((self.cant_loc_con_coordenadas / (self.cant_loc_con_coordenadas + self.cant_loc_sin_coordenadas)) * 100, 2)

    def devolver_lista_municipios(self):
        """
        Devuelve la lista de municipios.
        """
        return self.lista_municipios
    
    def devolver_estadisticas(self):
        """
        Devuelve las estadisticas de los datos cargados.
        """
        return self.cantidad_municipios, self.cant_loc_sin_coordenadas, self.cant_loc_con_coordenadas

    def imprimir_datos(self):
        """
        Imprime los datos cargados.
        """
        for municipio in self.lista_municipios:
            print(f"Municipio: {municipio.nombre}, Localidad: {municipio.localidad}, Coordenadas: ({municipio.longitud}, {municipio.latitud})")

    def mostrar_estadisticas(self):
        """
        Imprime las estadisticas de los datos cargados.
        """
        print(f"Cantidad de municipios: {self.cantidad_municipios}")
        print(f"Cantidad de localidades: {self.cant_loc_con_coordenadas + self.cant_loc_sin_coordenadas}")
        print(f"Cantidad de localidades con coordenadas: {self.cant_loc_con_coordenadas}")
        print(f"Cantidad de localidades sin coordenadas: {self.cant_loc_sin_coordenadas}")
        print(f"Porcentaje de localidades con coordenadas: {self.porc_loc_con_coordenadas}%")
        print(f"Porcentaje de localidades sin coordenadas: {self.porc_loc_sin_coordenadas}%")

class Municipio:
    """
    Esta clase se encarga de almacenar los datos de un municipio.
    """
    def __init__(self, nombre, longitud, latitud, localidad):
        """
        Inicializa la clase.
        :param nombre: Nombre del municipio.
        :param longitud: Longitud del municipio.
        :param latitud: Latitud del municipio.
        :param localidad: Localidad del municipio.
        """
        self.nombre = nombre
        self.longitud = longitud
        self.latitud = latitud
        self.localidad = localidad

# Crear un objeto de la clase Main
main = Main("zonas_caracas.json")

# Cargar los datos
main.cargar_datos()

# Mostrar las estadisticas
main.mostrar_estadisticas()