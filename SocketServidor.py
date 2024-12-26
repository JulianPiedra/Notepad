import socket
import base64
import threading
import configparser
from datetime import datetime
import json
from pymongo import MongoClient
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import xmltodict
class Archivos():
    def ingresarDocumentoCifrado(contenido):
        try:
            cliente = MongoClient("mongodb://localhost:27017/")
            db = cliente["DBCifrador"]
            coleccion = db["Archivos"]
            nombreDocumento = contenido["_id"]
            documentoExistente = coleccion.find_one({"_id": nombreDocumento})

            if documentoExistente:
                mensaje = "El nombre ya existe en la base de datos."
                return mensaje
            else:
                mensaje = "Documento guardado correctamente"
                coleccion.insert_one(contenido)
                return mensaje
        except Exception as e:
            return e
    
    def ListarDocumentos():
        try:
            cliente = MongoClient("mongodb://localhost:27017/")
            db = cliente["DBCifrador"]
            coleccion = db["Archivos"]
            documentos = coleccion.find({}, {"_id": 1}) 
            listaDocumentos = []
            for documento in documentos:
                listaDocumentos.append(str(documento["_id"])) 
            
            root = Element('documentos')
            
            for id in listaDocumentos:
                documento = SubElement(root, 'documento')
                documento.text = id
            
            xml_str = tostring(root, encoding='utf8').decode('utf8')
            
            xml_str = parseString(xml_str).toprettyxml(indent="   ")
            
            return xml_str
        except Exception as e:
            return str(e)
    def ObtenerDocumentos(contenido):
        try:
            cliente = MongoClient("mongodb://localhost:27017/")
            db = cliente["DBCifrador"]
            coleccion = db["Archivos"]
            nombreDocumento = contenido["_id"]
            documento = coleccion.find_one({"_id": nombreDocumento})
            
            documento_dict = {
                "_id": str(documento["_id"]),
                "Contenido": str(documento["contenido"]),
                "TipoCifrado": str(documento["tipoCifrado"]),
                "Clave": str(documento["clave"])
            }

            xml_string = xmltodict.unparse({"Documento": documento_dict}, pretty=True)

            return xml_string

        except Exception as e:
            return str(e)
    
    def ActualizarDocumentos(contenido):
        try:
            cliente = MongoClient("mongodb://localhost:27017/")
            db = cliente["DBCifrador"]
            coleccion = db["Archivos"]
            nombreDocumento = contenido["_id"]
            documentoExistente = coleccion.find_one({"_id": nombreDocumento})

            if documentoExistente:    
                mensaje = "Documento actualizado correctamente"
                coleccion.update_one({"_id": nombreDocumento}, {"$set": contenido})
                return mensaje
            else:
                mensaje = "El nombre no existe en la base de datos."
                return mensaje
                
        except Exception as e:
            return e
        
def handle_client(client_socket, client_address):
    try:
        print(f"Conexión establecida desde {client_address}")
        datosJson = client_socket.recv(1024).decode()
        contenido = json.loads(datosJson)
        print("Mensaje recibido:", contenido)
    except Exception as e:
        return e
    try:
        archivo = Archivos
        if contenido.get("accion") == "guardar":
            contenido.pop("accion")
            respuesta = archivo.ingresarDocumentoCifrado(contenido)
            client_socket.sendall(respuesta.encode())
        elif contenido.get("accion")=="listar":
            respuesta = archivo.ListarDocumentos()
            client_socket.sendall(respuesta.encode())
        elif contenido.get("accion")=="obtener":
            contenido.pop("accion")
            respuesta = archivo.ObtenerDocumentos(contenido)
            client_socket.sendall(respuesta.encode())
        elif contenido.get("accion")=="actualizar":
            contenido.pop("accion")
            respuesta = archivo.ActualizarDocumentos(contenido)
            client_socket.sendall(respuesta.encode())
    finally:
            client_socket.close()

config = configparser.ConfigParser()
config.read('config.ini')
Host = config.get('Settings', 'Host')
Puerto = config.get('Settings', 'Puerto')

# Crear un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlazar el socket al host y puerto especificados
server_socket.bind((Host, int(Puerto)))

# Configurar el socket para aceptar conexiones entrantes
server_socket.listen(10)  # El argumento indica el número máximo de conexiones en cola

print(f"Servidor escuchando en {Host}:{Puerto}")

try:
    while True:
        # Esperar a que llegue una conexión
        client_socket, client_address = server_socket.accept()

        # Manejar la conexión en un hilo separado
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
except KeyboardInterrupt:
    print("Servidor detenido.")
finally:
    # Cerrar el socket del servidor
    server_socket.close()
