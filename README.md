# Archivo de prueba para el uso de JSON en Python

## Descripción del Programa

Este archivo es un programa en Python que permite obtener información meteorológica de diferentes localidades. 

## Instalar módulos Necesarios

```bash
pip install requests
pip install matplotlib
```

## Ejecutable .exe (Opcional)
Usando pyinstaller puedes crear un ejecutable por si no quieres abrir el programa con la terminal/cmd.

### Instalar pyinstaller
```bash
pip install pyinstaller
```

### Crear un archivo .exe a partir de un archivo .py

Linux

```bash
pyinstaller -F --add-data "data.json:." app.py
```


Windows

```bash
pyinstaller -F --add-data "data.json;." app.py
```