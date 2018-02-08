<<<<<<< HEAD
from ftplib import FTP #Libreria utilizada para conectarse a un servidor FTP y obtener informacion
import os #Libreria utilizada para crear carpetas de almacenamiento
import requests #Libreria utilizada para obtener el url
import sys #Libreria utilizada para obtener el codigo obtenido
from api import claves #Importa la api
=======
from ftplib import FTP 
import os 
import sys 
from api import claves 


def main():
    print(fecha)
    cinco_dias(fecha)
    descarga_datos(fecha)
>>>>>>> chely2

def fecha_usr(ip): #Obtener fecha del url

    conexion = FTP(ip) #Nombre del servidor
    conexion.login(clave.usr, clave.pwd) #Usuario y contrasena del servidor
    fecha = [] 
    conexion.dir(fecha.append) #Se almacena toda la informacion que se encuentra en el directorio actual dentro del arreglo
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

def descarga_datos(fecha):
    try:
        conexion=FTP(clave.ip);
        conexion.login(clave.usr,clave.pwd)
        print("Conexion exitosa")

        conexion.cwd('{}'.format(fecha))

        if os.path.exists('data'):
            os.chdir('data')
        else:
            os.mkdir('data')
            os.chdir('data') 
        if os.path.exists('{}'.format(fecha)):
            for i in range(1,6):
<<<<<<< HEAD
=======
                print("Descargando archivo d{}.txt".format(i))
>>>>>>> chely2
                conexion.retrbinary('RETR d{}.txt'.format(i),open('{}/d{}.txt'.format(fecha, i),'wb').write)
        else:
            os.mkdir('{}'.format(fecha))
            for i in range(1,6):
<<<<<<< HEAD
                conexion.retrbinary('RETR d{}.txt'.format(i),open('{}/d{}.txt'.format(fecha, i), 'wb').write)
        conexion.quit()
        os.chdir('..')

=======
                print("Descargando archivo d{}.txt".format(i))
                conexion.retrbinary('RETR d{}.txt'.format(i),open('{}/d{}.txt'.format(fecha, i), 'wb').write)
        conexion.quit()
        os.chdir('..')
>>>>>>> chely2
    except ValueError:
        print("Conexion fallida")

clave=claves()
fecha=fecha_usr(clave.ip)
<<<<<<< HEAD
print(fecha)
print(cinco_dias(fecha))
descarga_datos(fecha)


=======

if __name__=="__main__":
    main() 
>>>>>>> chely2
