from api import claves
from ftplib import FTP 
import os 
import requests 
import sys #Librerias utilizadas


def obtener_fecha(ip): #Obtener la fecha actual
    ftp = FTP(ip) 
    ftp.login(cve.usr, cve.pwd) 
    fecha = [] 
    ftp.dir(fecha.append) #Se almacena toda la informacion que se encuentra en el directorio actual dentro del arreglo
    fecha = fecha[-1].split()[-1] #Se toma el ultimo valor del arreglo, se separa la cadena en un arreglo dividido por espacios y se toma el ultimo valor.
    return fecha # Se devuelve el valor obtenido
 
def cinco_dias(fecha): #Obtener cuatro dias posteriores a la fecha obtenida
    ano, mes, dia = (int(n) for n in fecha.split("-")) 
    if mes in (1, 3, 5, 7, 8, 10, 12): #Validacion de fecha 
        dias_mes = 31
    elif mes == 2:
        if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0): #Si el mes se visiesto
            dias_mes = 29
        else:
            dias_mes = 28
    elif mes in (4, 6, 9, 11):
        dias_mes = 30
    dias = [] 
    for n in range(0, 5): #Ciclo utilizado para almacenar los 5 dias
        if dia + n <= dias_mes:
            dias.append('{:04d}-{:02d}-{:02d}'.format(ano, mes, dia + n))
        else:                                                               
            if mes != 12:
                dias.append('{:04d}-{:02d}-{:02d}'.format(ano, mes+1, n - (dias_mes - dia)))
            else:
                dias.append('{:04d}-01-{:02d}'.format(ano + 1, n - (dias_mes - dia)))
    return dias

def descargar_docs(fecha): #Descargar los documentos de la carpeta con el nombre de la fecha actual
    ftp = FTP(cve.ip); 
    ftp.login(cve.usr, cve.pwd) 
    ftp.cwd('{}'.format(fecha)) 
    if os.path.exists('Descarga de archivos'): 
        os.chdir('Descarga de archivos')
    else:
        os.mkdir('Descarga de archivos') 
        os.chdir('Descarga de archivos') 
    if os.path.exists('{}'.format(fecha)): 
        os.chdir('{}'.format(fecha)) 
        for i in range(1, 6): #Ciclo que realiza 5 veces el proceso incrementando su valor 1
           print("DESGARGANDO INFORMACION DE DOCUMENTO d{}.txt".format(i))
                ftp.retrbinary('RETR d{}.txt'.format(i),open('d{}.txt'.format(i),'wb').write)
    else:
        os.mkdir('{}'.format(fecha)) 
        os.chdir('{}'.format(fecha)) 
        for i in range(1, 6): #Ciclo que realiza 5 veces el proceso incrementando su valor 1
           print("DESGARGANDO INFORMACION DE DOCUMENTO d{}.txt".format(i)) #Descarga los documentos
    ftp.quit()
    os.chdir('../..') 


cve = claves()
fecha = obtener_fecha(cve.ip)
print (fecha)
print (cinco_dias(fecha))
descargar_docs(fecha)