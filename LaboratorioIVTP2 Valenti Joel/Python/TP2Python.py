import requests 
import pymysql 
import sys

def crearBD():
        try:
            conexion= pymysql.connect(host="localhost", user="root", password="", db="mysql")
            cursor=conexion.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS python")
            conexion.close()
            cursor.close()
        except:
            print('Error al crear la base de datos')
def crearTabla():
        try:
            conexion= pymysql.connect(host="localhost", user="root", password="", db="python")
            cursor=conexion.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS pais (codigo INT(11) NOT NULL,nombrePais VARCHAR(50) NOT NULL,capitalPais VARCHAR(50) NOT NULL,region VARCHAR(50) NOT NULL, latitud FLOAT NOT NULL,longitud FLOAT NOT NULL,poblacion BIGINT,PRIMARY KEY(codigo,nombrePais))")
            conexion.close()
            cursor.close()
        except:
            print('Error al crear la tabla')

def insertarDatos(nombrePais, capitalPais, region, latitud, longitud, codigoPais, poblacion):
    try:
            conexion= pymysql.connect(host="localhost", user="root", password="", db="python")
            cursor=conexion.cursor()
            cursor.execute("INSERT INTO pais(codigo,nombrePais,capitalPais,region,latitud,longitud,poblacion) VALUES (%s,%s,%s,%s,%s,%s,%s)", (int(codigoPais),nombrePais,capitalPais,region,float(latitud),float(longitud),float((poblacion))))
            conexion.commit()
            conexion.close()
            cursor.close()
    except:
            e = sys.exc_info()
            print( e )

if __name__ == '__main__':
    
    crearBD()
    crearTabla()
    for i in range(300):
        url = 'https://restcountries.eu/rest/v2/callingcode/'+str(i)
        response = requests.get(url)
        if response.status_code == 200:
            response_jsons=dict()
            response_jsons=response.json()
            for response_json in response_jsons:
                nombrePais=response_json['name']
                capitalPais=response_json['capital']
                region=response_json['region']
                latitud=response_json['latlng'][0]
                longitud=response_json['latlng'][1]
                codigoPais=i
                poblacion=response_json['population']
                print(str(codigoPais))
                insertarDatos(nombrePais, capitalPais, region, latitud, longitud, codigoPais, poblacion)
    print()
    