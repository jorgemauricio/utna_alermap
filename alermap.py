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
    mapa(fecha)

def fecha_usr(ip)

    conexion = FTP(ip) 
    conexion.login(clave.usr, clave.pwd)
    fecha = []
    conexion.dir(fecha.append) 
    fecha = fecha[-1].split()[-1] 
    return fecha 


def cinco_dias(fecha): #Obtener cuatro dias posteriores a la fecha obtenida

    ano, mes, dia = (int(n) for n in fecha.split("-")) 
    if mes in (1, 3, 5, 7, 8, 10, 12):
        dias_mes = 31
    elif mes == 2:
        if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0): 
            dias_mes = 29
        else:
            dias_mes = 28
    elif mes in (4, 6, 9, 11):
        dias_mes = 30
    dias = []
    for n in range(0, 5): 
        if dia + n <= dias_mes:
            dias.append('{:04d}-{:02d}-{:02d}'.format(ano, mes, dia + n)) 
        else:                                                               
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
    df = pd.DataFrame()
    variables=['Rain', 'Tmin', 'Tmax', 'Windpro']
    
    for x in range(0,5):
        datos = pd.read_csv('data/{}/d{}.txt'.format(fecha, x))
        for j in range(0, 5):
            x= np.array(datos['Long'])
            y= np.array(datos['Lat'])
            x_min=x.min()
            x_max=x.max()
            y_min=y.min()
            y_max=y.max()
            lista= variable(variables[x])
            var1=datos.loc[datos[variables[x]] >= lista[0]]
            var1=var1.loc[var1[variables[x]] <= lista[1]]
            var2=datos.loc[datos[variables[x]] >= lista[2]]
            var2=var2.loc[var2[variables[x]] <= lista[3]]
            var3=datos.loc[datos[variables[x]] >= lista[4]]
            var3=var3.loc[var3[variables[x]] <= lista[5]]
            var4=datos.loc[datos[variables[x]] >= lista[6]]
            var4=var4.loc[var4[variables[x]] <= lista[7]]
            var5=datos.loc[datos[variables[x]] >= lista[8]]
            var5=var5.loc[var5[variables[x]] <= lista[9]]
            map = Basemap(projection ='mill', llcrnrlat=y_min,urcrnrlat=y_max,llcrnrlon=x_min,urcrnrlon=x_max,resolution='c')
            x, y=map(x,y)
            map.scatter(x,y, marker='.', color='{}'. format(lista))
            map.readshapefile('utna_alermap/shapes/Estados','Mill')
            print ('Generando Mapa "Pronostico del dia {} - {}.png" ...'.format(fecha[i]))
            plt.title('Pronostico de clima Alermap \n {}'.format(cinco_dias[i]))
            plt.savefig("mapas/{}/Pronostico de Alermap - {}.png".format(fecha, cincodias[i]))
                   
def variable(vari):
    lista=[]
    if vari =='Rain':
        return lista=[20, 50, 50, 70, 70, 100, 100, 150, 150, 300,'rainbow']
    
    elif vari=='Windpro':
        return lista=[62, 74, 74, 88, 88, 102, 102, 117, 117, 150, 'Wistia']

    elif vari=='Tmin':
        return lista=[3, 0, 0, -3, -3, -6, -6, -9, -9, -12, 'winter']

    elif vari=='Tmax':
        return lista=[30, 35, 35, 40, 40, 45, 45, 50, 50, 55, 'YIOrRd']


clave=claves()
fecha=fecha_usr(clave.ip)
print(fecha)
print(cinco_dias(fecha))
descarga_datos(fecha)
mapa(fecha)

if __name__=="__main__":
    main()
