from ftplib import FTP
import os
import sys
from api import claves
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap


def main():
    print(fecha)
    cinco_dias(fecha)
    descarga_datos(fecha)

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
                print("Descargando archivo d{}.txt".format(i))
                conexion.retrbinary('RETR d{}.txt'.format(i),open('{}/d{}.txt'.format(fecha, i),'wb').write)
        else:
            os.mkdir('{}'.format(fecha))
            for i in range(1,6):
                print("Descargando archivo d{}.txt".format(i))
                conexion.retrbinary('RETR d{}.txt'.format(i),open('{}/d{}.txt'.format(fecha, i), 'wb').write)
        conexion.quit()
        os.chdir('..')
    except ValueError:
        print("Conexion fallida")

def mapa(fecha):
    
    if os.path.exists('mapas'):
        os.chdir('mapas')
    else:
        os.mkdir('mapas')
        os.chdir('mapas')
    os.chdir("..")

    variables=['Rain', 'Tmin', 'Tmax', 'Windpro']
    for x in range(1,6):
        datos = pd.read_csv('data/{}/d{}.txt'.format(fecha, x))
        x= np.array(datos['Long'])
        x_min=x.min()
        x_max=x.max()
        y= np.array(datos['Lat'])
        y_min=y.min()
        y_max=y.max()

        for v in variables:
            if v =='Rain':
                var1=datos.loc[datos['Rain']>=20]
                var1=var1.loc[var1['Rain']<=50]
                var2=datos.loc[datos['Rain']>=50]
                var2=var2.loc[var2['Rain']<=70]
                var3=datos.loc[datos['Rain']>=70]
                var3=var3.loc[var3['Rain']<=150]
                var4=datos.loc[datos['Rain']>=150]
                var4=var4.loc[var4['Rain']<=300]
                var5=datos.loc[datos['Rain']>=300]

            elif v =='Windpro':
                var1=datos.loc[datos['Windpro']>=50]
                var1=var1.loc[var1['Windpro']>=61]
                var2=datos.loc[datos['Windpro']>=62]
                var2=var2.loc[var2['Windpro']>=74]
                var3=datos.loc[datos['Windpro']>=75]
                var3=var3.loc[var3['Windpro']>=88]
                var4=datos.loc[datos['Windpro']>=89]
                var4=var4.loc[var4['Windpro']>=102]
                var5=datos.loc[datos['Windpro']>=102]
                var5=var5.loc[var5['Windpro']>=117]

            elif v =='Tmin':
                var1=datos.loc[datos['Tmin']>=-9]
                var1=var1.loc[var1['Tmin']<=-6]
                var2=datos.loc[datos['Tmin']>=-6]
                var2=var2.loc[var2['Tmin']<=-3]
                var3=datos.loc[datos['Tmin']>=-3]
                var3=var3.loc[var3['Tmin']<=0]
                var4=datos.loc[datos['Tmin']>=0]
                var4=var4.loc[var4['Tmin']<=3]
                var5=datos.loc[datos['Tmin']>=3]
                var5=var5.loc[var5['Tmin']<=6]

            elif v=='Tmax':

                var1=datos.loc[datos['Tmax']>=30]
                var1=var1.loc[var1['Tmax']<=35]
                var2=datos.loc[datos['Tmax']>=35]
                var2=var2.loc[var2['Tmax']<=40]
                var3=datos.loc[datos['Tmax']>=40]
                var3=var3.loc[var3['Tmax']<=45]
                var4=datos.loc[datos['Tmax']>=45]
                var4=var4.loc[var4['Tmax']<=50]
                var5=datos.loc[datos['Tmax']>=50]
               

            x=np.array(var1['Long'])
            y=np.array(var1['Lat'])

            map = Basemap(projection ='mill', llcrnrlat=y_min,urcrnrlat=y_max,llcrnrlon=x_min,urcrnrlon=x_max,resolution='c')
            x, y=map(x,y)
            map.scatter(x,y, marker='.', color='#0404B4')
            map.readshapefile('utna_alermap/shapes/Estados','Mill')
            plt.show()


clave=claves()
fecha=fecha_usr(clave.ip)
print(fecha)
print(cinco_dias(fecha))
descarga_datos(fecha)
mapa(fecha)

if __name__=="__main__":
    main()
