from flask import Flask, request, jsonify
import sqlite3
import mysql.connector
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins='http://localhost:4200')

@app.route('/votos', methods=['POST'])
def recibir_votos():
    # Obtiene los datos del voto desde el cuerpo de la solicitud
    datos_voto = request.json

    # Persiste los datos del voto en la base de datos
    persistir_voto(datos_voto)

    # Envía una respuesta al votante para confirmar la recepción del voto
    respuesta = {'mensaje': '¡Tu voto ha sido registrado correctamente!'}
    return jsonify(respuesta), 200

@app.route('/votos', methods=['GET'])
def mostrar_votos():
    # Obtiene los datos de los votos desde la base de datos
    votos = obtener_votos()

    # Envía una respuesta con los votos obtenidos
    respuesta = {'votos': votos}
    return jsonify(respuesta), 200

def persistir_voto(datos_voto):
    # Conectarse a la base de datos
    conexion = mysql.connector.connect(
        host='localhost',
        user='Alcornoque',
        password='alcornoque123',
        database='votacion'
    )
    cursor = conexion.cursor()

    # Crear la tabla de votos si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS votos
                      (id INT AUTO_INCREMENT PRIMARY KEY,
                       nombre VARCHAR(50),
                       opcion VARCHAR(50))''')

    # Insertar los datos del voto en la tabla
    nombre = datos_voto['nombre']
    opcion = datos_voto['opcion']
    cursor.execute("INSERT INTO votos (nombre, opcion) VALUES (%s, %s)", (nombre, opcion))

    # Confirmar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()

def obtener_votos():
    # Conectarse a la base de datos
    conexion = mysql.connector.connect(
        host='localhost',
        user='Alcornoque',
        password='alcornoque123',
        database='votacion'
    )
    cursor = conexion.cursor()

    # Obtener los votos de la tabla
    cursor.execute("SELECT * FROM votos")
    votos = cursor.fetchall()

    # Cerrar la conexión
    conexion.close()

    return votos

if __name__ == '__main__':
    app.run()