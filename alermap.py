from ftplib import FTP
import os
import sys
from api import claves
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib  import cm
import shapefile
                                                                #Librerias utilizadas


def main():
    #fecha='2018-04-25'
    clave=claves()
    fecha=fecha_usr(clave)
    print(cinco_dias(fecha))
    cincodias = cinco_dias(fecha)
    descarga=descarga_datos(fecha, clave)
    mapa(fecha,cincodias)

def fecha_usr(clave):   #Obtener fecha del url
    conexion = FTP(clave.ip)   #Nombre del servidor
    conexion.login(clave.usr, clave.pwd)  #Usuario y contrasena del servidor
    fecha = []
    conexion.dir(fecha.append)  #Se almacena toda la informacion que se encuentra en el directorio actual dentro del arreglo
    fecha = fecha[-1].split()[-1]
    print("Obteniendo fecha actual:'{}'".format(fecha))
    return fecha  # Se devuelve el valor obtenido


def cinco_dias(fecha): #Funcion para obtener cuatro dias posteriores a la fecha obtenida

    ano, mes, dia = (int(n) for n in fecha.split("-")) 
    if mes in (1, 3, 5, 7, 8, 10, 12):  #Validacion de fecha
        dias_mes = 31
    elif mes == 2:
        if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0): 
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

def descarga_datos(fecha, clave): #Descargar los documentos de la carpeta con el nombre de la fecha actual
    try:
        conexion=FTP(clave.ip);   #Nombre del servidor
        conexion.login(clave.usr,clave.pwd)  #Usuario y contrasena del servidor
        print("Conexion exitosa")
        conexion.cwd('{}'.format(fecha))     #Infresa a una carpeta dentro del servidor

 
        if os.path.exists('data'):  #verifica si existe la carpeta data  (donde se almacenaran los documentos a descargar)
            os.chdir('data')       #Accede a la carpeta data
        else:
            os.mkdir('data')        #Si no existe crea la carpeta data
            os.chdir('data')        #Accede a la carpeta data
        if os.path.exists('{}'.format(fecha)): #Ingresar a la carpeta fecha
            for i in range(1,6):
                print("Descargando archivo d{}.txt".format(i))
                conexion.retrbinary('RETR d{}.txt'.format(i),open('{}/d{}.txt'.format(fecha, i),'wb').write)
        else:
            os.mkdir('{}'.format(fecha))
            for i in range(1,6): #Ciclo utilizado para descargaar los cinco archivos .txt
                print("Descargando archivo d{}.txt".format(i))
                conexion.retrbinary('RETR d{}.txt'.format(i),open('{}/d{}.txt'.format(fecha, i), 'wb').write)
        conexion.quit()
        os.chdir('..')
    except ValueError:
        print("Conexion fallida") # sino hay internet marca error 

def mapa(fecha, cincodias): #funcion de creacion de mapas
    
   

    variables=['Rain', 'Tmin', 'Tmax', 'Windpro']
    titulos=['Precipitación Acumulada en 24h','Temperatura Minima en 24h','Temperatura Máxima en 24 h','Velocidad del viento promedio en 24h']
    val=['mm', '°C ', '°C ', 'km/h']

    for i in range(1,6):  # ciclo para leer los 5 archivos .txt
        datos = pd.read_csv('data/{}/d{}.txt'.format(fecha,i)) 
        long = np.array(datos['Long'])
        lat = np.array(datos['Lat'])
        long_min=long.min()
        long_max=long.max()
        lat_min=lat.min()
        lat_max=lat.max()
        print('Generando mapas del dia {}'.format(i))  #mensaje que imprime para decir cuales mapas se estan creando
        for j in range(0,4):#ciclo para crear los cinco mapas por cada variable 
            map = Basemap(projection ='mill', llcrnrlat=lat_min,urcrnrlat=lat_max, 
                llcrnrlon=long_min, urcrnrlon=long_max,resolution='c')
            lista = rangos(variables[j])
            col = colores(variables[j])
            print('Generando mapas de variable: {}'.format(variables[j]))
            a = 0
            b = 1
            c = 0
            for k in range(1, 6):# ciclo para mapear la informacion en cad uno de los mapas
                alermap = datos.loc[datos[variables[j]] >= lista[a]]
                alermap = alermap.loc[alermap[variables[j]] <= lista[b]]
                x, y = map(np.array(alermap['Long']), np.array(alermap['Lat']))
                map.scatter(x, y, marker='o', color=col[c], s=1)
                z=np.array([lista[0], lista[-1]])
                colorbar=cm.rainbow(z/ float(max(z)))
                plot=plt.scatter(z,z, c=z, cmap=col[-1])
                a = a + 2
                b = b + 2
                c = c + 1
            cb1=plt.colorbar(plot) #barra de colores
            cb1.set_label(' {}'.format(val[j]))
            map.readshapefile('shapes/Estados','Mill')# lellendo el shapefile 
            plt.text(x =1.0536e+06, y =1.33233e+06, s = u' @2018 INIFAP', fontsize = 15 ,color='green') #marca de agua
            plt.title('{} para el dia \n {} '.format(titulos[j], cincodias[i-1])) #titulo de los mapas
            if os.path.exists('mapas'):  #verifica si existe la carpeta data  (donde se almacenaran los documentos a descargar)
                os.chdir('mapas') #Accede a la carpeta data
            else:
                os.mkdir('mapas') #Si no existe crea la carpeta data
                os.chdir('mapas')  #Accede a la carpeta data
            os.chdir("..")
            plt.savefig('mapas/Pronostico-del-dia-{}-clima-{}.png'.format(cincodias[i-1], variables[j]),dpi=300)
            plt.title('{} para el dia \n {} '.format(titulos[j], cincodias[i-1]))
         
            plt.clf()


def rangos(var):#funcion de rangos para cada variable
    lista=[]
    if var =='Rain':
        lista=[20, 50, 50, 70, 70, 100, 100, 150, 150, 300,300,500]
    
    elif var=='Windpro':
        lista=[62, 74, 74, 88, 88, 102, 102, 117, 117, 150]

    elif var=='Tmin':
        lista=[3, 0, 0, -3, -3, -6, -6, -9, -9, -12]

    elif var=='Tmax':
        lista=[30, 35, 35, 40, 40, 45, 45, 50, 50, 55]
    return lista
    
def colores(var): #funcion de colores 
    if var=='Rain':
        colores=['purple','royalblue', 'aqua', 'orange', 'red', 'rainbow']
        
    if var=='Windpro':
        colores=['yellow', 'gold', 'orange', 'darkorange', 'orangered', 'Wistia']
        
    if var=='Tmin':
        colores=['darkblue', 'blue', 'royalblue', 'dodgerblue', 'cyan', 'winter']
        
    if var=='Tmax':
        colores=['darkorange', 'orangered', 'tomato', 'red', 'darkred', 'YlOrRd']
    return colores
                

if __name__=="__main__":
    main()
