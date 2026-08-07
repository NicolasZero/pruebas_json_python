# Librerias
from pathlib import Path
import sys
import json
import os
import requests # No nativo
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt

# Definicion de constantes
class Constantes:
    """
    Definicion de constantes para el programa.
    """
    YEAR_MIN = 2022
    YEAR_MAX = 2026
    RUTA_ARCHIVO = "data.json"
    URL_API = "https://api.open-meteo.com/v1/forecast"
    URL_API_HISTORIC = "https://historical-forecast-api.open-meteo.com/v1/forecast"
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
    MESES ={
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }

# Para la lista de objetos de localidades
class Localidad:
    """
    Localidad: nombre, municipio y coordenadas (longitud y latitud).
    """
    def __init__(self, nombre, municipio, longitud, latitud, clima=None, temperatura=None, viento=None, humedad=None):
        self.nombre = nombre
        self.municipio = municipio
        self.longitud = longitud
        self.latitud = latitud
        self.clima = clima
        self.temperatura = temperatura
        self.viento = viento
        self.humedad = humedad

    def agregar_clima(self, clima):
        """
        define el clima del objeto
        """
        self.clima = clima

    def agregar_temperatura(self, temperatura):
        """
        define la temperatura del objeto
        """
        self.temperatura = temperatura

    def agregar_viento(self, viento):
        """
        define el viento del objeto
        """
        self.viento = viento

    def agregar_humedad(self, humedad):
        """
        define la humedad del objeto
        """
        self.humedad = humedad
    
    def imprimir_datos(self):
        """
        imprime los datos del objeto
        """
        print("\n\033[1;32m----- DATOS -----\033[0m")
        print(f"Nombre: \033[1;34m{self.nombre}\033[0m")
        print(f"Municipio: \033[1;34m{self.municipio}\033[0m")
        print(f"Longitud: \033[1;34m{self.longitud or 'No hay datos'}\033[0m")
        print(f"Latitud: \033[1;34m{self.latitud or 'No hay datos'}\033[0m")
        print(f"Clima: \033[1;34m{self.clima or 'No hay datos'}\033[0m")
        print(f"Temperatura: \033[1;34m{self.temperatura or 'No hay datos'}\033[0m")
        print(f"Viento: \033[1;34m{self.viento or 'No hay datos'}\033[0m")
        print(f"Humedad: \033[1;34m{self.humedad or 'No hay datos'}\033[0m")

# Clase separada para leer el json
class LeerJSON:
    """
    Gestiona la lectura del archivo JSON.
    """
    def __init__(self):
        self.ruta_archivo = Constantes.RUTA_ARCHIVO

    def cargar_datos(self):
        """
        carga los datos del archivo JSON
        :return: lista de localidades
        """
        localidades = []

        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = Path(__file__).parent
        self.ruta_archivo = os.path.join(base_path, "data.json")

        if not os.path.isfile(self.ruta_archivo):
            return localidades

        with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        
        for municipio in datos:
            for localidad in datos[municipio]:
                localidades.append(Localidad(localidad['localidad'], municipio, localidad['longitud'], localidad['latitud']))
        
        return localidades

# Separado de main para las estadisticas
class Estadisticas:
    """
    Se encarga exclusivamente de calcular y almacenar las estadisticas sobre las localidades.
    """
    def __init__(self, lista_localidades):
        self.lista_localidades = lista_localidades
        self.total_municipios = len(set(loc.municipio for loc in lista_localidades))
        self.total_localidades = len(lista_localidades)
        self.con_coordenadas = sum(1 for loc in lista_localidades if loc.longitud is not None and loc.latitud is not None)
        self.sin_coordenadas = self.total_localidades - self.con_coordenadas
        self.porc_con_coordenadas = round((self.con_coordenadas / self.total_localidades) * 100, 2) if self.total_localidades > 0 else 0.0
        self.porc_sin_coordenadas = round((self.sin_coordenadas / self.total_localidades) * 100, 2) if self.total_localidades > 0 else 0.0

    def mostrar_estadisticas(self):
        """
        muestra las estadisticas de las localidades
        """
        print("\033[1;32m<----- ESTADISTICAS ----->\033[0m")
        print(f" - Total de municipios: \033[1;34m{self.total_municipios}\033[0m")
        print(f" - Total de localidades: \033[1;34m{self.total_localidades}\033[0m")
        print(f" - Localidades con coordenadas: \033[1;34m{self.con_coordenadas} ({self.porc_con_coordenadas}%)\033[0m")
        print(f" - Localidades sin coordenadas: \033[1;34m{self.sin_coordenadas} ({self.porc_sin_coordenadas}%)\033[0m")

    def temperatura_alta(self):
        """
        devuelve la temperatura alta
        """
        print(f"\033[1;32m<----- TEMPERATURA MAS ALTA ----->\033[0m\n")
        print("Temperatura - Localidad - Municipio")
        lista_temperaturas = [f"{i.temperatura}°C | {i.nombre} | {i.municipio}" for i in self.lista_localidades if i.temperatura is not None]
        lista_temperaturas.sort(reverse=True)
        if len(lista_temperaturas) == 0:
            print("\033[1;34m No hay datos para calcular la temperatura mas alta\033[0m")
        else:
            limite = len(lista_temperaturas)
            if limite > 10:
                limite = 10
            for i in range(limite):
                print(lista_temperaturas[i])
    
    def temperatura_baja(self):
        """
        devuelve la temperatura baja
        """
        print(f"\033[1;32m<----- TEMPERATURA MAS BAJA ----->\033[0m\n")
        print("Temperatura - Localidad - Municipio")
        lista_temperaturas = [f" {i.temperatura}°C | {i.nombre} | {i.municipio}" for i in self.lista_localidades if i.temperatura is not None]
        lista_temperaturas.sort()
        if len(lista_temperaturas) == 0:
            print("\033[1;34m No hay datos para calcular la temperatura mas baja\033[0m")
        else:
            limite = len(lista_temperaturas)
            if limite > 10:
                limite = 10
            for i in range(limite):
                print(lista_temperaturas[i])

    def temperatura_promedio(self):
        """
        muestra la temperatura promedio
        """
        lista_temperaturas = [i.temperatura for i in self.lista_localidades if i.temperatura is not None]
        print(f"\033[1;32m<----- TEMPERATURA PROMEDIO DEL HISTORIAL ----->\033[0m\n")
        if len(lista_temperaturas) == 0:
            print("\033[1;34m No hay datos para calcular la temperatura promedio\033[0m")
        else:
            temp_prom = sum(lista_temperaturas) / len(lista_temperaturas)
            print(f"La temperatura promedio del historial es de \033[1;34m{temp_prom}°C\033[0m")

    def procesar_registros_grafica(self, registros):
        """
        Procesa los registros de las localidades y muestra las estadisticas.
        :param registros: Lista de registros
        """
        # temperatura maxima
        temp_max_unidad = 0
        temp_max_year = None
        # temperatura minima 
        temp_min_unidad = 0
        temp_min_year = None
        # viento maximo
        viento_max_unidad = 0
        viento_max_year = None
        # viento minimo
        viento_min_unidad = 0
        viento_min_year = None

        # humedad maxima
        humedad_max_unidad = 0
        humedad_max_year = None
        # humedad minima
        humedad_min_unidad = 0
        humedad_min_year = None
        # precipitacion
        precipitacion_unidad = 0
        precipitacion_year = None

        lista_years = []
        lista_datos_graficos = []

        for year in registros:
            lista_years.append(year.year)
            dato_grafico = []
            for mes in year.registros_mensuales:
                temperatura_acumulada = 0
                viento_acumulado = 0
                humedad_acumulada = 0
                precipitacion_acumulada = 0
                
                for registro in mes.registros:
                    temperatura_acumulada += registro.temperatura_pro
                    viento_acumulado += registro.viento_pro
                    humedad_acumulada += registro.humedad_pro
                    precipitacion_acumulada += registro.precipitacion

                    # Comprobar si es la temperatura máxima
                    if registro.temperatura_max > temp_max_unidad or temp_max_year is None:
                        temp_max_unidad = registro.temperatura_max
                        temp_max_year = year.year

                    # Comprobar si es la temperatura mínima
                    if registro.temperatura_min < temp_min_unidad or temp_min_year is None:
                        temp_min_unidad = registro.temperatura_min
                        temp_min_year = year.year

                    # Comprobar si es el viento máximo
                    if registro.viento_max > viento_max_unidad or viento_max_year is None:
                        viento_max_unidad = registro.viento_max
                        viento_max_year = year.year

                    # Comprobar si es el viento mínimo
                    if registro.viento_min < viento_min_unidad or viento_min_year is None:
                        viento_min_unidad = registro.viento_min
                        viento_min_year = year.year

                    # Comprobar si es la humedad máxima
                    if registro.humedad_max > humedad_max_unidad or humedad_max_year is None:
                        humedad_max_unidad = registro.humedad_max
                        humedad_max_year = year.year

                    # Comprobar si es la humedad mínima
                    if registro.humedad_min < humedad_min_unidad or humedad_min_year is None:
                        humedad_min_unidad = registro.humedad_min
                        humedad_min_year = year.year

                    # Comprobar si es la precipitación
                    if registro.precipitacion > precipitacion_unidad or precipitacion_year is None:
                        precipitacion_unidad = registro.precipitacion
                        precipitacion_year = year.year

                temperatura_promedio = (temperatura_acumulada / len(mes.registros))
                viento_promedio = (viento_acumulado / len(mes.registros))
                humedad_promedio = (humedad_acumulada / len(mes.registros))
                precipitacion_promedio = (precipitacion_acumulada / len(mes.registros))

                # Guardamos el nombre del mes y los promedios
                dato_grafico.append([Constantes.MESES[mes.mes], precipitacion_promedio, temperatura_promedio, viento_promedio, humedad_promedio])

            lista_datos_graficos.append(dato_grafico)

        print("\n\033[1;32m----- SELECCIONA UN AÑO -----\033[0m")
        for i in range(len(lista_years)):
            print(f"  {i+1}. Año {lista_years[i]}")
        print("  0. Volver al menu principal")

        interfaz = Interfaz()
        selec = input("\nSeleccione el numero del año que desea ver: ")
        if selec.isdigit():
            if int(selec) == 0:
                pass
            elif int(selec) > 0 and int(selec) <= len(lista_years):
                interfaz.mostrar_grafico_magnitudes(lista_datos_graficos[int(selec)-1], lista_years[int(selec)-1])
            else:
                interfaz.imprimir_error("El año seleccionado no existe")
        else:
            interfaz.imprimir_error("Seleccione un año valido")

# Clase para obtener los datos del clima
class Clima:
    """
    Gestiona la obtención de datos del clima de una localidad.
    """
    def __init__(self):
        self._url_api = Constantes.URL_API
        self._url_api_historica = Constantes.URL_API_HISTORIC

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
            url = f"{self._url_api}?latitude={localidad.latitud}&longitude={localidad.longitud}&current=weather_code,temperature_2m,wind_speed_10m,relative_humidity_2m"
            response = requests.get(url)
            datos = response.json()
            clima = Constantes.WEATHER_CODE[datos["current"]["weather_code"]]
            localidad.agregar_clima(clima)
            localidad.agregar_temperatura(datos["current"]["temperature_2m"])
            localidad.agregar_viento(datos["current"]["wind_speed_10m"])
            localidad.agregar_humedad(datos["current"]["relative_humidity_2m"])
            print(f"El clima en \033[1;34m{localidad.nombre}\033[0m es \033[1;34m{clima}\033[0m con una temperatura de \033[1;34m{localidad.temperatura}°C\033[0m")
            print(f"La humedad es de \033[1;34m{localidad.humedad}%\033[0m y el viento es de \033[1;34m{localidad.viento} km/h\033[0m")
            # return f"El clima en {localidad.nombre} es: {clima}"
        except Exception:
            return "Error al obtener los datos del clima"

    def obtener_clima_periodo(self, localidad, fecha_inicio, fecha_fin):
        """
        Obtiene los datos del clima para un rango de fechas.
        :param localidad: Localidad para la cual obtener los datos del clima.
        :param fecha_inicio: Fecha de inicio del rango.
        :param fecha_fin: Fecha de fin del rango.
        :return: Diccionario con los datos del clima.
        """
        if localidad.latitud is None or localidad.longitud is None:
            return "No se pueden obtener los datos del clima para esta localidad porque no tiene coordenadas."
        
        # Try para manejar el error con la api
        try:
            print(f"\n\nbuscando datos del clima desde \033[1;34m{fecha_inicio}\033[0m hasta \033[1;34m{fecha_fin}\033[0m en \033[1;34m{localidad.nombre}\033[0m...\n")
            url = f"{self._url_api_historica}?latitude={localidad.latitud}&longitude={localidad.longitud}&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,wind_speed_10m_min,relative_humidity_2m_max,relative_humidity_2m_min,precipitation_sum&start_date={fecha_inicio}&end_date={fecha_fin}"
            response = requests.get(url)
            datos = response.json()

            cant_result = len(datos["daily"]["time"])

            lista_diaria = []
            lista_mensual = []
            lista_anual = []

            mes_prev = 1
            year_prev = int(fecha_inicio.split("-")[0])
            
            for i in range(cant_result):
                mes_tmp = int(datos["daily"]["time"][i].split("-")[1])
                year_tmp = int(datos["daily"]["time"][i].split("-")[0])

                temperatura_max = datos["daily"]["temperature_2m_max"][i] or 0
                temperatura_min = datos["daily"]["temperature_2m_min"][i] or 0

                viento_max = datos["daily"]["wind_speed_10m_max"][i] or 0
                viento_min = datos["daily"]["wind_speed_10m_min"][i] or 0

                humedad_max = datos["daily"]["relative_humidity_2m_max"][i] or 0
                humedad_min = datos["daily"]["relative_humidity_2m_min"][i] or 0

                precipitacion = datos["daily"]["precipitation_sum"][i] or 0

                temperatura_pro = (temperatura_max + temperatura_min) / 2
                viento_pro = (viento_max + viento_min) / 2
                humedad_pro = (humedad_max + humedad_min) / 2

                # cambio de año
                if year_prev != year_tmp or i == cant_result - 1:
                    lista_diaria.append(Registro(temperatura_max, temperatura_min, viento_max, viento_min, humedad_max, humedad_min, precipitacion))
                    mes = RegistroMensual(mes_prev, lista_diaria)
                    lista_mensual.append(mes)
                    lista_diaria = []
                    mes_prev = mes_tmp

                    year = RegistroAnual(year_prev, lista_mensual)
                    lista_anual.append(year)
                    lista_mensual = []
                    year_prev = year_tmp
                
                # cambio de mes
                if mes_prev != mes_tmp:
                    mes = RegistroMensual(mes_prev, lista_diaria)
                    lista_mensual.append(mes)
                    lista_diaria = []
                    mes_prev = mes_tmp

                lista_diaria.append(Registro(temperatura_max, temperatura_min, viento_max, viento_min, humedad_max, humedad_min, precipitacion))

            return lista_anual
        except Exception as e:
            return f"Error al obtener los datos del clima: {e}"

class RegistroAnual:
    """
    Registro anual: año y registros mensuales.
    """
    def __init__(self, year, registros_mensuales):
        self.year = year
        self.registros_mensuales = registros_mensuales

class RegistroMensual:
    """
    Registro mensual: mes y registros diarios.
    """
    def __init__(self, mes, registros):
        self.mes = mes
        self.registros = registros

class Registro:
    """
    Registro: temperatura_pro, temperatura_max, temperatura_min, viento_pro, viento_max, viento_min, humedad_pro, humedad_max, humedad_min, precipitacion.
    """
    def __init__(self, temperatura_max, temperatura_min, viento_max, viento_min, humedad_max, humedad_min, precipitacion):
        self.temperatura_pro = (temperatura_max + temperatura_min) / 2
        self.temperatura_max = temperatura_max
        self.temperatura_min = temperatura_min
        self.viento_pro = (viento_max + viento_min) / 2
        self.viento_max = viento_max
        self.viento_min = viento_min
        self.humedad_pro = (humedad_max + humedad_min) / 2
        self.humedad_max = humedad_max
        self.humedad_min = humedad_min
        self.precipitacion = precipitacion

#  Para gestionar la interfaz
class Interfaz:
    """
    Maneja toda la interacción con el usuario a través de la consola.
    """
    def limpiar_pantalla(self):
        """
        Limpia la pantalla de la consola.
        """
        if os.name == 'nt':
            # si es Windows
            os.system('cls')
        else:
            # si es Linux o MacOS
            os.system('clear')

    def mostrar_registros(self, registros):
        """
        Muestra un resumen de los registros anuales.
        """
        # temperatura maxima
        temp_max_unidad = 0
        temp_max_year = None
        # temperatura minima 
        temp_min_unidad = 0
        temp_min_year = None
        # viento maximo
        viento_max_unidad = 0
        viento_max_year = None
        # viento minimo
        viento_min_unidad = 0
        viento_min_year = None

        # humedad maxima
        humedad_max_unidad = 0
        humedad_max_year = None
        # humedad minima
        humedad_min_unidad = 0
        humedad_min_year = None
        # precipitacion
        precipitacion_unidad = 0
        precipitacion_year = None

        lista_years = []
        lista_datos_graficos = []

        print("\n\033[1;33m--------- REGISTROS ANUALES --------\033[0m")
        for year in registros:
            print(f"-------\033[1;34m Año {year.year} \033[0m--------")
            lista_years.append(year.year)
            dato_grafico = []
            for mes in year.registros_mensuales:
                temperatura_acumulada = 0
                viento_acumulado = 0
                humedad_acumulada = 0
                precipitacion_acumulada = 0
                
                print(f"\n-> Mes \033[1;34m{Constantes.MESES[mes.mes]}\033[0m")
                # print(f"Cantidad de registros: {len(mes.registros)}")
                for registro in mes.registros:
                    temperatura_acumulada += registro.temperatura_pro
                    viento_acumulado += registro.viento_pro
                    humedad_acumulada += registro.humedad_pro
                    precipitacion_acumulada += registro.precipitacion

                    # Comprobar si es la temperatura máxima
                    if registro.temperatura_max > temp_max_unidad or temp_max_year is None:
                        temp_max_unidad = registro.temperatura_max
                        temp_max_year = year.year

                    # Comprobar si es la temperatura mínima
                    if registro.temperatura_min < temp_min_unidad or temp_min_year is None:
                        temp_min_unidad = registro.temperatura_min
                        temp_min_year = year.year

                    # Comprobar si es el viento máximo
                    if registro.viento_max > viento_max_unidad or viento_max_year is None:
                        viento_max_unidad = registro.viento_max
                        viento_max_year = year.year

                    # Comprobar si es el viento mínimo
                    if registro.viento_min < viento_min_unidad or viento_min_year is None:
                        viento_min_unidad = registro.viento_min
                        viento_min_year = year.year

                    # Comprobar si es la humedad máxima
                    if registro.humedad_max > humedad_max_unidad or humedad_max_year is None:
                        humedad_max_unidad = registro.humedad_max
                        humedad_max_year = year.year

                    # Comprobar si es la humedad mínima
                    if registro.humedad_min < humedad_min_unidad or humedad_min_year is None:
                        humedad_min_unidad = registro.humedad_min
                        humedad_min_year = year.year

                    # Comprobar si es la precipitación
                    if registro.precipitacion > precipitacion_unidad or precipitacion_year is None:
                        precipitacion_unidad = registro.precipitacion
                        precipitacion_year = year.year

                temperatura_promedio = (temperatura_acumulada / len(mes.registros))
                viento_promedio = (viento_acumulado / len(mes.registros))
                humedad_promedio = (humedad_acumulada / len(mes.registros))
                precipitacion_promedio = (precipitacion_acumulada / len(mes.registros))

                # Guardamos el nombre del mes y los promedios
                dato_grafico.append([Constantes.MESES[mes.mes], precipitacion_promedio, temperatura_promedio, viento_promedio, humedad_promedio])

                print(f"     Temperatura promedio:\033[1;34m {temperatura_promedio:.2f} \033[0m")
                print(f"     Viento promedio:\033[1;34m {viento_promedio:.2f} \033[0m")
                print(f"     Humedad promedio:\033[1;34m {humedad_promedio:.2f} \033[0m")
                print(f"     Precipitación promedio:\033[1;34m {precipitacion_promedio:.2f} \033[0m")
            lista_datos_graficos.append(dato_grafico)
            
        print(f"\n\033[1;32m----- Estadisticas generales (no promedios) -----\033[0m")
        print(f"- Temperatura maxima:\033[1;34m {temp_max_unidad} ({temp_max_year}) \033[0m")
        print(f"- Temperatura minima:\033[1;34m {temp_min_unidad} ({temp_min_year}) \033[0m")
        print(f"- Viento maximo:\033[1;34m {viento_max_unidad} ({viento_max_year}) \033[0m")
        print(f"- Viento minimo:\033[1;34m {viento_min_unidad} ({viento_min_year}) \033[0m")
        print(f"- Humedad maxima:\033[1;34m {humedad_max_unidad} ({humedad_max_year}) \033[0m")
        print(f"- Humedad minima:\033[1;34m {humedad_min_unidad} ({humedad_min_year}) \033[0m")
        print(f"- Precipitacion:\033[1;34m {precipitacion_unidad} ({precipitacion_year}) \033[0m")

        print("\n\033[1;32m----- GRAFICA DE LOS AÑOS -----\033[0m")
        for i in range(len(lista_years)):
            print(f"  {i+1}. Año {lista_years[i]}")
        print("  0. Volver al menu principal")

        selec = input("\nSeleccione el numero del año que desea ver: ")
        if selec.isdigit():
            if int(selec) == 0:
                pass
            elif int(selec) > 0 and int(selec) <= len(lista_years):
                self.mostrar_grafico_magnitudes(lista_datos_graficos[int(selec)-1], lista_years[int(selec)-1])
            else:
                self.imprimir_error("El año seleccionado no existe")
        else:
            self.imprimir_error("Seleccione un año valido")

    def mostrar_grafico_magnitudes(self, dato_grafico, year=""):
        """
        Muestra un grafico de las temperaturas.
        """
        if not dato_grafico:
            print("No hay datos para graficar.")
            return

        meses = [d[0] for d in dato_grafico]
        precipitaciones = [d[1] for d in dato_grafico]
        temperaturas = [d[2] for d in dato_grafico]
        vientos = [d[3] for d in dato_grafico]
        humedades = [d[4] for d in dato_grafico]

        fig, ax = plt.subplots(figsize=(10, 6))
        fig.subplots_adjust(right=0.75)

        twin1 = ax.twinx()
        twin2 = ax.twinx()
        twin3 = ax.twinx()

        twin2.spines.right.set_position(("axes", 1.12))
        twin3.spines.right.set_position(("axes", 1.24))

        x = list(range(len(meses)))

        p1, = ax.plot(x, precipitaciones, "C0", marker="o", label="Precipitacion")
        p2, = twin1.plot(x, temperaturas, "C1", marker="s", label="Temperatura")
        p3, = twin2.plot(x, vientos, "C2", marker="^", label="Viento")
        p4, = twin3.plot(x, humedades, "C3", marker="d", label="Humedad")

        ax.set_title(f"Promedio de magnitudes del año {year}", fontsize=14, fontweight='bold')
        ax.set_xlabel("Meses")
        
        ax.set_xticks(x)
        ax.set_xticklabels(meses, rotation=30, ha='right')

        ax.set_ylabel("Precipitacion (mm)")
        twin1.set_ylabel("Temperatura (°C)")
        twin2.set_ylabel("Viento (km/h)")
        twin3.set_ylabel("Humedad (%)")

        ax.yaxis.label.set_color(p1.get_color())
        twin1.yaxis.label.set_color(p2.get_color())
        twin2.yaxis.label.set_color(p3.get_color())
        twin3.yaxis.label.set_color(p4.get_color())

        ax.tick_params(axis='y', colors=p1.get_color())
        twin1.tick_params(axis='y', colors=p2.get_color())
        twin2.tick_params(axis='y', colors=p3.get_color())
        twin3.tick_params(axis='y', colors=p4.get_color())

        lines = [p1, p2, p3, p4]
        labels = [l.get_label() for l in lines]
        ax.legend(lines, labels, loc='upper left')

        plt.tight_layout()
        plt.show()

    def imprimir_menu(self, titulo, opciones):
        """
        Imprime un menu con las opciones dadas.
        :param titulo: titulo del menu
        :param opciones: lista de opciones
        """
        print(f"\n\033[1;32m<----- {titulo} ----->\033[0m\n")
        for i, opcion in enumerate(opciones):
            print(f"  \033[1;33m{i+1}.-\033[0m {opcion}")
        print("  \033[1;33m0.-\033[0m Volver al menu principal")
        return input("\nElige una opcion: \033[1;33m")

    def menu_principal(self):
        """
        Muestra el menu principal y retorna la opcion elegida.
        """
        titulo = "MENÚ PRINCIPAL"
        opciones = ["Ver localidades", "Ver estadisticas", "Ver historial", "Ver meteorologia"]
        return self.imprimir_menu(titulo, opciones)

    def sub_menu_estadisticas(self):
        """
        Muestra el sub menu de estadisticas y retorna la opcion elegida.
        """
        titulo = "ESTADÍSTICAS"
        opciones = ["Ver temperatura mas alta", "Ver temperatura mas baja", "Ver estadisticas de las localidades"]
        return self.imprimir_menu(titulo, opciones)

    def sub_menu_historial(self):
        """
        Muestra el sub menu de historial y retorna la opcion elegida.
        """
        titulo = "HISTORIAL"
        opciones = ["Ver historial", "Ver temperatura promedio del historial"]
        return self.imprimir_menu(titulo, opciones)

    def sub_menu_localidades(self):
        """
        Muestra el sub menu de localidades y retorna la opcion elegida.
        """
        titulo = "LOCALIDADES"
        opciones = ["Buscar por nombre", "Ver todas las localidades", "Ver localidades sin coordenadas"]
        return self.imprimir_menu(titulo, opciones)

    def sub_menu_clima(self):
        """
        Muestra el sub menu de clima y retorna la opcion elegida.
        """
        titulo = "CLIMA"
        opciones = ["Seleccionar por municipio", "Buscar por nombre", "Ver por periodo de tiempo", "Ver grafica"]
        return self.imprimir_menu(titulo, opciones)

    def esperar_enter(self):
        """
        Espera a que el usuario presione Enter para continuar.
        """
        input("\n\033[1;33m Presiona Enter para continuar...\033[0m")

    def seleccionar_rango_tiempo(self):
        """
        Solicita al usuario que ingrese un rango de años y lo valida.
        :return: el año de inicio y el año de fin.
        """
        print("\n\033[1;32m----- SELECCIONAR RANGO DE TIEMPO -----\033[0m")
        print(f"Datos disponibles desde el año {Constantes.YEAR_MIN} hasta el año actual")

        # Para mayor comodidad se pide solo el año y asi solo son dos inputs en vez de 6
        a_inicio = input(f"\nDesde enero 1 del año (por defecto {Constantes.YEAR_MIN}): ")
        a_fin = input(f"Hasta diciembre 31 del año (por defecto {Constantes.YEAR_MIN}): ")

        a_inicio = a_inicio or str(Constantes.YEAR_MIN)
        a_fin = a_fin or str(Constantes.YEAR_MIN)

        # Valida que los años sean digitos
        if a_inicio.isdigit() and a_fin.isdigit():
            a_inicio = int(a_inicio)
            a_fin = int(a_fin)
            # Valida que los años esten dentro del rango permitido
            if a_inicio < Constantes.YEAR_MIN or a_fin > Constantes.YEAR_MAX:
                self.imprimir_error(f"Los años deben estar entre {Constantes.YEAR_MIN} y {Constantes.YEAR_MAX}.")
                return None, None
            # Valida que el año de inicio sea menor que el año de fin
            if a_inicio > a_fin:
                self.imprimir_error("El año inicial debe ser menor que el año final.")
                return None, None
            # Retorna las fechas en formato AAAA-MM-DD
            fecha_inicio = f"{a_inicio}-01-01"
            fecha_fin = f"{a_fin}-12-31"
            # fecha_fin = f"{a_fin}-02-28"
            return fecha_inicio, fecha_fin
        else:
            self.imprimir_error("Por favor, ingrese números válidos.")
            return None, None

    def seleccionar_municipio(self, lista_municipios, lista_localidades, con_coordenadas=True, mostrar_todo=False):
        """
        Selecciona una localidad del municipio seleccionado por el usuario
        """
        print("\033[1;32m----- SELECCIONAR MUNICIPIO -----\033[0m")
        for i, municipio in enumerate(lista_municipios):
            print(f"  {i + 1}. {municipio}")
        print("  0. Volver al menu principal")
        
        eleccion = input("\nSeleccione un municipio (por defecto 1): ")
        eleccion = eleccion or "1"

        if not eleccion.isdigit():
            self.imprimir_error("Por favor, ingrese un número.")
            return None
        eleccion = int(eleccion)

        if eleccion == 0:
            return None

        if eleccion < 1 or eleccion > len(lista_municipios):
            self.imprimir_error("El número seleccionado no es válido.")
            return None
        
        municipio_seleccionado = lista_municipios[eleccion - 1]
        encontradas = []

        print("\n\033[1;32m----- SELECCIONAR LOCALIDAD -----\033[0m")
        print(f"Localidades del municipio \033[1;34m{municipio_seleccionado}\033[0m:")
        # Filtrar e imprimir localidades del municipio seleccionado
        for i, localidad in enumerate(lista_localidades):
            if localidad.municipio == municipio_seleccionado:
                # Se muestran todas las localidades
                if mostrar_todo:
                    encontradas.append(localidad)
                # Se muestran solo las localidades con coordenadas
                elif con_coordenadas and localidad.latitud is not None and localidad.longitud is not None:
                    encontradas.append(localidad)
                # Se muestran solo las localidades sin coordenadas
                elif not con_coordenadas and (localidad.latitud is None or localidad.longitud is None):
                    encontradas.append(localidad)

        for i, localidad in enumerate(encontradas):
            print(f"  {i + 1}. {localidad.nombre}")
        print("  0. Volver al menu principal")

        eleccion2 = input("\nSeleccione una localidad (por defecto 1): ")
        eleccion2 = eleccion2 or "1"
        
        if not eleccion2.isdigit():
            self.imprimir_error("Por favor, ingrese un número!")
            return None
        eleccion2 = int(eleccion2)
        
        if eleccion2 == 0:
            return None

        if eleccion2 < 1 or eleccion2 > len(encontradas):
            self.imprimir_error("El número seleccionado no es válido!")
            return None
            
        return encontradas[eleccion2 - 1]

    def buscar_localidad(self, lista_localidades, mostrar_todo=False):
        """
        Busca una localidad por nombre.
        :return: la localidad encontrada.
        """
        print("\033[1;32m----- BUSCAR LOCALIDAD -----\033[0m")
        nombre_busqueda = input("Ingrese el nombre de la localidad: ").strip().lower()
        encontradas = []

        for localidad in lista_localidades:
            if nombre_busqueda in localidad.nombre.lower():
                if mostrar_todo:
                    encontradas.append(localidad)
                    print(f"  {len(encontradas)}. {localidad.nombre} - {localidad.municipio}")
                elif localidad.latitud is not None and localidad.longitud is not None:
                    encontradas.append(localidad)
                    print(f"{len(encontradas)}. {localidad.nombre} - {localidad.municipio}")

        if len(encontradas) == 0:
            print("\033[1;31mLocalidad no encontrada.\033[0m")
            return None

        print("  0. Volver al menu principal")
        
        print(f"\nSe encontraron {len(encontradas)} localidades.")
        eleccion = input("Ingrese el número de la localidad que desea seleccionar (por defecto 1): ")
        eleccion = eleccion or "1"
        
        if not eleccion.isdigit():
            self.imprimir_error("Por favor, ingrese un número!")
            return None
        eleccion = int(eleccion)
        if eleccion == 0:
            return None
        if eleccion < 1 or eleccion > len(encontradas):
            self.imprimir_error("El número seleccionado no es válido!")
            return None
            
        return encontradas[eleccion - 1]

    def imprimir_lista(self, lista_datos):
        """
        Imprime una lista de datos.
        """
        if lista_datos:
            for i, valor in enumerate(lista_datos):
                print(f"{i + 1}. {valor}")
        else:
            print("No hay datos para mostrar.")

    def imprimir_error(self, error):
        """
        Imprime un mensaje de error en color rojo.
        """
        print(f"\n\t \033[91mError: {error}\033[0m")

class Historial:
    def __init__(self):
        self.historial = []
    
    def agregar_historial(self, localidad):
        """
        Agrega una localidad al historial
        """
        # Comprobar si la localidad ya esta en el historial y actualizarla
        for i, j in enumerate(self.historial):
            if localidad.nombre == j.nombre and localidad.municipio == j.municipio:
                self.historial[i] = localidad
                break
        else:  # Si no se encontro la localidad
            self.historial.append(localidad)

    def mostrar_historial(self):
        """
        Muestra el historial de consultas
        """
        print(f"\n\033[1;32m<----- HISTORIAL DE CONSULTAS ----->\033[0m")
        if self.historial:
            for i in self.historial:
                print(f"\033[1;34m{i.nombre} - {i.municipio}\033[0m: \n -> Clima: \033[1;34m{i.clima}\033[0m, Temperatura: \033[1;34m{i.temperatura}°C\033[0m, Viento: \033[1;34m{i.viento} km/h\033[0m, Humedad: \033[1;34m{i.humedad}%\033[0m")
        else:
            print("\n  \033[1;34mNo hay historial de consultas\033[0m")

    def obtener_historial(self):
        """
        Retorna el historial de consultas
        """
        return self.historial

#  Para la aplicacion principal
class Aplicacion:
    """
    Controla la aplicacion
    """
    def __init__(self):
        self.archivo = LeerJSON()
        self.interfaz = Interfaz()
        self.servicio_clima = Clima()
        self.historial = Historial()
        self.localidades = []
        self.municipios = []
        self.activo = True # Para el menu

    def iniciar(self):
        # LIMPIAR PANTALLA
        self.interfaz.limpiar_pantalla()
        # Cargar datos
        self.localidades = self.archivo.cargar_datos()
        # Se cambio como se genera la lista de municipios
        vistos = set()
        self.municipios = []
        for loc in self.localidades:
            if loc.municipio not in vistos:
                vistos.add(loc.municipio)
                self.municipios.append(loc.municipio)

        stats = Estadisticas(self.localidades)

        # Ciclo del menú principal
        while self.activo:
            # Estadisticas
            stats.mostrar_estadisticas()
            # Menu - interfaz
            opcion = self.interfaz.menu_principal()
            # Limpiar pantalla
            self.interfaz.limpiar_pantalla()
            
            # Menu localidades
            if opcion == "1":
                while True:
                    opcion_sub = self.interfaz.sub_menu_localidades()
                    self.interfaz.limpiar_pantalla()
                    localidad = None
                    # Por municipio
                    if opcion_sub == "1":
                        localidad = self.interfaz.buscar_localidad(self.localidades, True)

                    # Todas las localidades
                    elif opcion_sub == "2":
                        localidad = self.interfaz.seleccionar_municipio(self.municipios, self.localidades, True, True)

                    # Localidades sin coordenadas
                    elif opcion_sub == "3":
                        localidad = self.interfaz.seleccionar_municipio(self.municipios, self.localidades, False, False)

                    if localidad:
                        localidad.imprimir_datos()

                    if opcion_sub == "0":
                        break
                    self.interfaz.esperar_enter()
                    self.interfaz.limpiar_pantalla()
                    
            # Menu estadisticas
            elif opcion == "2":
                while True:
                    opcion_sub = self.interfaz.sub_menu_estadisticas()

                    self.interfaz.limpiar_pantalla()
                    if opcion_sub == "1":
                        Estadisticas(self.historial.obtener_historial()).temperatura_alta()

                    elif opcion_sub == "2":
                        Estadisticas(self.historial.obtener_historial()).temperatura_baja()

                    elif opcion_sub == "3":
                        stats.mostrar_estadisticas()
            
                    elif opcion_sub == "0":
                        break

                    self.interfaz.esperar_enter()
                    self.interfaz.limpiar_pantalla()
                    
            # Historial
            elif opcion == "3":
                while True:
                    opcion_sub = self.interfaz.sub_menu_historial()
                    self.interfaz.limpiar_pantalla()
                    
                    if opcion_sub == "1":
                        self.historial.mostrar_historial()
                        self.interfaz.esperar_enter()
                    
                    elif opcion_sub == "2":
                        rank = Estadisticas(self.historial.obtener_historial())
                        rank.temperatura_promedio()
                        self.interfaz.esperar_enter()
                    
                    elif opcion_sub == "0":
                        break
                    
                    self.interfaz.limpiar_pantalla()

            # Menu clima
            elif opcion == "4":
                while True:
                    opcion_sub = self.interfaz.sub_menu_clima()
                    self.interfaz.limpiar_pantalla()

                    # Seleccionar
                    if opcion_sub == "1":
                        localidad = self.interfaz.seleccionar_municipio(self.municipios, self.localidades)
                        if localidad:
                            self.servicio_clima.obtener_clima(localidad)
                            self.historial.agregar_historial(localidad)

                    # Buscar por nombre
                    elif opcion_sub == "2":
                        localidad = self.interfaz.buscar_localidad(self.localidades)
                        if localidad:
                            self.servicio_clima.obtener_clima(localidad)
                            self.historial.agregar_historial(localidad)

                    # Rango de tiempo 
                    elif opcion_sub == "3":
                        localidad = self.interfaz.seleccionar_municipio(self.municipios, self.localidades)
                        
                        if localidad:
                            fecha_inicio, fecha_fin = self.interfaz.seleccionar_rango_tiempo()
                            if fecha_inicio and fecha_fin:
                                registros = self.servicio_clima.obtener_clima_periodo(localidad, fecha_inicio, fecha_fin)
                                self.interfaz.mostrar_registros(registros)
                    
                    # grafica
                    elif opcion_sub == "4":
                        localidad = self.interfaz.seleccionar_municipio(self.municipios, self.localidades)
                        
                        if localidad:
                            fecha_inicio, fecha_fin = self.interfaz.seleccionar_rango_tiempo()
                            if fecha_inicio and fecha_fin:
                                registros = self.servicio_clima.obtener_clima_periodo(localidad, fecha_inicio, fecha_fin)
                                stats.procesar_registros_grafica(registros)
                    
                    elif opcion_sub == "0":
                        break
                    
                    self.interfaz.esperar_enter()
                    self.interfaz.limpiar_pantalla()
            
            elif opcion == "0":
                self.activo = False
                print("\033[0mSaliendo del programa...")
                break
            # else:
            #     self.interfaz.imprimir_error("Opción no válida. Intenta de nuevo.")
            #     self.interfaz.esperar_enter()
            
            self.interfaz.limpiar_pantalla()

# Ejecutar el aplicacion
app = Aplicacion()
app.iniciar()