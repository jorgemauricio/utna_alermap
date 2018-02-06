from ftplib import FTP #Libreria utilizada para conectarse a un servidor FTP y obtener informacion
import os #Libreria utilizada para crear carpetas de almacenamiento
import requests #Libreria utilizada para obtener el url
import sys #Libreria utilizada para obtener el codigo obtenido
from api import clave #Importa la api

def fecha_usr(ip): #Obtener fecha del url

    conexion = FTP(ip) #Nombre del servidor
    conexion.login(clave.usr, clave.pwd) #Usuario y contrasena del servidor
    fecha = [] 
    ftp.dir(fecha.append) #Se almacena toda la informacion que se encuentra en el directorio actual dentro del arreglo
    fecha = fecha[-1].split()[-1] #Se toma el ultimo valor del arreglo, se separa la cadena en un arreglo dividido por espacios y se toma el ultimo valor.
    return fecha # Se devuelve el valor obtenido
    

def cinco_dias(fecha): #Obtener cuatro dias posteriores a la fecha obtenida
    ano, mes, dia = (int(n) for n in fecha.split("-")) #Almacenamos cada dato correspondiente dividiendolo por un (-) 
    if mes in (1, 3, 5, 7, 8, 10, 12): #Validacion de fecha 
        dias_mes = 31
    elif mes == 2:
        if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0): #Si el mes se bisiesto
            dias_mes = 29
        else:
            dias_mes = 28
    elif mes in (4, 6, 9, 11):
        dias_mes = 30
    dias = [] 
    for n in range(0, 5): #Ciclo utilizado para almacenar los 5 dias
        if dia + n <= dias_mes:
            dias.append('{:04d}-{:02d}-{:02d}'.format(ano, mes, dia + n)) #'{:04d}-{:02d}-{:02d}' - Formato para la fecha
        else:                                                               #Agrega un cero en el caso de los nuemeros unicos entre 1 - 9
            if mes != 12:
                dias.append('{:04d}-{:02d}-{:02d}'.format(ano, mes+1, n - (dias_mes - dia)))
            else:
                dias.append('{:04d}-01-{:02d}'.format(ano + 1, n - (dias_mes - dia)))
    return dias

def descargar_datos(fecha):    	
    try:
        conexion = FTP(ip)
        conexion.login(clave.usr, clave.pwd)
        print("conexion exitosa")
    except ValueError:
         print("conexion fallida")

    conexion.cwd('{}'.format(fecha)) #Ingresa a una carpeta dentro del servidor
	
    if os.path.exists('datos'):
    #Verifica si la carpeta datos existe (donde se almacenaran los documentos a descargar)
		os.chdir('datos') #Accede a la carpeta datos
	else:
		os.mkdir('datos') #Crea la carpeta datos 
		os.chdir('datos') #Accede a la carpeta datos
	if os.path.exists('{}'.format(fecha)): 
		for i in range(1, 6): #Ciclo que realiza 5 veces el proceso incrementando su valor 1
		    ftp.retrbinary('RETR d{}.txt'.format(i),open('{}/d{}.txt'.format(fecha, i),'wb').write) #Descarga los documentos
	else:
		os.mkdir('{}'.format(fecha)) #Crea la carpeta fecha donde se almacenaran los documentos
		for i in range(1, 6): #Ciclo que realiza 5 veces el proceso incrementando su valor 1
           ftp.retrbinary('RETR d{}.txt'.format(i),open('{}/d{}.txt'.format(fecha, i),'wb').write) #Descarga los documentos

	ftp.quit()
	os.chdir('..') #Sale de la carpeta datos al directorio raiz


clave=claves()
fecha=fecha_usr(clave.ip)
print(fecha)
print(cinco_dias(fecha))
descargar_datos(fecha)

