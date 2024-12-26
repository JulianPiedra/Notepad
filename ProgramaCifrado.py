import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from PIL import Image, ImageTk
import configparser
import socket
import pymongo
import json
from xml.etree import ElementTree
#Variable global
archivoActual = None  

#**********************************************************************

#Funciones de Archivo
def abrirArchivo():
    global archivoActual
    archivoTxt = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    if archivoTxt:
        try:
            with open(archivoTxt, "r") as documentoTxt:
                contenidoTxt = documentoTxt.read()
                editorTexto.delete("1.0", tk.END) 
                editorTexto.insert(tk.END, contenidoTxt)  
                archivoActual = archivoTxt
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{str(e)} \nSELECCIONE UN ARCHIVO  DE FORMATO .txt")

def guardarArchivo():
    global archivoActual
    if archivoActual:
        try:
            with open(archivoActual, "w") as documento:
                contenido = editorTexto.get("1.0", tk.END)
                documento.write(contenido)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
    else:
        guardarComoArchivo()

def guardarComoArchivo():
    global archivoActual
    archivoTxt = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    if archivoTxt:
        try:
            with open(archivoTxt, "w") as documento:
                contenido = editorTexto.get("1.0", tk.END)
                documento.write(contenido)
                archivoActual = archivoTxt  
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")

def nuevoArchivo():
    global archivoActual, nuevo, obtenido, id, clave, tipoCifrado
    nuevo = True
    obtenido = False
    clave = ""
    tipoCifrado = ""
    id= ""
    editorTexto.delete("1.0", tk.END) 
    archivoActual = None  

def salirAplicacion():
    confirmacion = messagebox.askyesno("Salir", "¿Realmente desea cerrar el programa y perder sus cambios?")
    if confirmacion:
        ventanaPrincipal.destroy()
#**********************************************************************

#Funciones de herramientas 
def cortarTexto():
    textoSeleccionado = editorTexto.get(tk.SEL_FIRST, tk.SEL_LAST)
    
    ventanaPrincipal.clipboard_clear()
    ventanaPrincipal.clipboard_append(textoSeleccionado)
    ventanaPrincipal.update()

    editorTexto.delete(tk.SEL_FIRST, tk.SEL_LAST)

def copiarTexto():
    textoSeleccionado = editorTexto.get(tk.SEL_FIRST, tk.SEL_LAST)

    ventanaPrincipal.clipboard_clear()
    ventanaPrincipal.clipboard_append(textoSeleccionado)
    ventanaPrincipal.update()

def pegarTexto():
    textoPortapapeles = ventanaPrincipal.clipboard_get()
    editorTexto.insert(tk.INSERT, textoPortapapeles)

#**********************************************************************

#Funciones de Cifrado
#Variable global    
abc = "abcdefghijklmnopqrstuvwxyz"
tipoCifrado = ""
clave = ""
obtenido = False
nuevo= True
id=""

def cifradoMonoalfabetico():
    global abc, tipoCifrado, clave, obtenido
    if not obtenido:
        clave = simpledialog.askstring("Clave", "Ingrese la clave numérica para el cifrado:")
    if clave is None:
        return
    elif len(clave) > 0:
        tipoCifrado = "Monoalfabetico"
        textoCifrado = ""
        texto = editorTexto.get("1.0", "end-1c")
        texto = texto.lower()
        for letra in texto:
            if letra in abc:
                suma = abc.find(letra) + int(clave)
                modulo = suma % len(abc)
                textoCifrado += abc[modulo]
            else:
                textoCifrado += letra
        editorTexto.delete("1.0", "end")
        editorTexto.insert("1.0", textoCifrado)
    else:
        messagebox.showerror("Error", "No se ingresó ninguna clave.")

def descifradoMonoalfabetico():
    global abc, obtenido, clave
        
    if not obtenido:
        clave = simpledialog.askstring("Clave", "Ingrese la clave numérica para el descifrado:")
    if clave is None:
        return
    elif len(clave) > 0:
        obtenido = False
        textoDescifrado = ''
        texto = editorTexto.get("1.0", "end-1c")
        texto = texto.lower()
        for letra in texto:
            if letra in abc:
                resta = abc.find(letra) - int(clave)
                modulo = resta % len(abc)
                textoDescifrado += abc[modulo]
            else:
                textoDescifrado += letra
        editorTexto.delete("1.0", "end")
        editorTexto.insert("1.0", textoDescifrado)
    else:
        messagebox.showerror("Error", "No se ingresó ninguna clave.")



def cifradoPolialfabetico():
    global abc, tipoCifrado, clave, obtenido
    if not obtenido:
        clave = simpledialog.askstring("Clave", "Ingrese la palabra clave para el cifrado:")
    if clave is None:
        return
    elif len(clave) > 0:
        tipoCifrado = "Polialfabetico"
        textoCifrado = ""
        texto = editorTexto.get("1.0", "end-1c")
        texto = texto.lower()
        indiceClave = 0
        for letra in texto:
            if letra in abc:
                if clave[indiceClave % len(clave)] == 'a':
                    desplazamiento = indiceClave % len(abc) 
                else:
                    desplazamiento = abc.find(clave[indiceClave % len(clave)])
                suma = abc.find(letra) + desplazamiento
                modulo = suma % len(abc)
                textoCifrado += abc[modulo]
                indiceClave += 1
            else:
                textoCifrado += letra
        editorTexto.delete("1.0", "end")
        editorTexto.insert("1.0", textoCifrado)
    else:
        messagebox.showerror("Error", "No se ingresó ninguna clave.")


def descifradoPolialfabetico():
    global abc, obtenido, clave
    if not obtenido:
        clave = simpledialog.askstring("Clave", "Ingrese la palabra clave para el descifrado:")
    if clave is None:
        return
    elif len(clave) > 0:
        obtenido = False
        textoDescifrado = ""
        texto = editorTexto.get("1.0", "end-1c")
        texto = texto.lower()
        indiceClave = 0
        for letra in texto:
            if letra in abc:
                if clave[indiceClave % len(clave)] == 'a':
                    desplazamiento = indiceClave % len(abc)  
                else:
                    desplazamiento = abc.find(clave[indiceClave % len(clave)])
                resta = abc.find(letra) - desplazamiento
                modulo = resta % len(abc)
                textoDescifrado += abc[modulo]
                indiceClave += 1
            else:
                textoDescifrado += letra
        editorTexto.delete("1.0", "end")  
        editorTexto.insert("1.0", textoDescifrado) 
    else:
        messagebox.showerror("Error", "No se ingresó ninguna clave.")



#**********************************************************************


#TAREA 3

# Ventana Configuracion         
def VentanaConfiguracion():
    ventanaConfiguracion = tk.Toplevel(ventanaPrincipal)
    ventanaConfiguracion.title("Configuración del servidor")
    ventanaConfiguracion.geometry('200x160+700+250')
    ventanaConfiguracion.configure(background="CadetBlue") 


    tk.Label(ventanaConfiguracion, text="Host:   ", background="CadetBlue").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(ventanaConfiguracion, text="Puerto:", background="CadetBlue").grid(row=1, column=0, padx=10, pady=10)

    txtHost = tk.Entry(ventanaConfiguracion)
    txtPuerto = tk.Entry(ventanaConfiguracion)

    txtHost.grid(row=0, column=1, padx=10, pady=10)
    txtPuerto.grid(row=1, column=1, padx=10, pady=10)

    # Obtener los valores actuales de Host y Puerto del archivo de configuración
    config = configparser.ConfigParser()
    config.read('config.ini')
    hostActual = config.get('Settings', 'Host')
    puertoActual = config.get('Settings', 'Puerto')

    # Establecer los valores actuales en los campos de entrada
    txtHost.insert(0, hostActual)
    txtPuerto.insert(0, puertoActual)

    # Crear botón para guardar la configuración
    botonGuardar = tk.Button(ventanaConfiguracion, background="Dark Green", text="Guardar", command=lambda: guardarConfiguracion(ventanaConfiguracion,txtHost.get(), txtPuerto.get()))
    botonGuardar.grid(row=2, column=0, columnspan=2, pady=10)



#Guardar el archivo de configuracion   
def guardarConfiguracion(ventana,host, puerto):
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Modificar los valores de Host y Puerto
    config.set('Settings', 'Host', host)
    config.set('Settings', 'Puerto', puerto)

    # Guardar los cambios en el archivo
    with open('config.ini', 'w') as archivoConfiguracion:
        config.write(archivoConfiguracion)

    messagebox.showinfo("Configuración actualizada", "La configuración ha sido actualizada correctamente.")    
    ventana.destroy()


#Ventana guardar en servidor
def ventanaGuardarEnServidor():
    global nuevo, id
    ventanaGuardarServidor = tk.Toplevel(ventanaPrincipal)
    ventanaGuardarServidor.title("Guardar en Servidor")
    ventanaGuardarServidor.geometry('370x200+700+250')
    ventanaGuardarServidor.configure(background="CadetBlue")        

    if nuevo==True:
        tk.Label(ventanaGuardarServidor, text="Nombre del documento:", background="CadetBlue").grid(row=0, column=0, padx=10, pady=10)
        txtNomDocumento = tk.Entry(ventanaGuardarServidor, width=30)
        txtNomDocumento.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(ventanaGuardarServidor, text="Elija una opcion de cifrado:", background="CadetBlue").grid(row=1, column=0, columnspan=2, pady=10)

        botonMono = tk.Button(ventanaGuardarServidor, background="Light Blue", text="Monoalfabetico", command=lambda: cifradoMonoalfabetico())
        botonMono.grid(row=2, column=0, padx=10, pady=10)
        botonPoli = tk.Button(ventanaGuardarServidor, background="Light Blue", text="Polialfabetico", command=lambda: cifradoPolialfabetico())
        botonPoli.grid(row=2, column=1, padx=10, pady=10)

        botonAceptar = tk.Button(ventanaGuardarServidor, background="Dark Green", text="Aceptar", command=lambda: guardarEnServidor(ventanaGuardarServidor, txtNomDocumento.get()))
        botonAceptar.grid(row=3,column=0,columnspan=2,pady=10)
    elif nuevo == False:
        botonAceptar = tk.Button(ventanaGuardarServidor, background="Dark Green", text="Actualizar", command=lambda: guardarEnServidor(ventanaGuardarServidor, id))
        botonAceptar.place(relx=0.5, rely=0.5, anchor="center")
        
        
def vetanaListarDesdeServidor():
    ventanaListar = tk.Toplevel(ventanaPrincipal)
    ventanaListar.title("Listar documentos")
    ventanaListar.geometry('250x500+700+250')
    ventanaListar.configure(background="CadetBlue")  
    
    label = tk.Label(ventanaListar, text="Elija el documento sobre el cual trabajar:", background="CadetBlue")
    label.place(relx=0.5, rely=0.1, anchor='n')  

    xml_string = listarDesdeServidor()
    
    root = ElementTree.fromstring(xml_string)
    id_doc = [elemento.text for elemento in root.findall('documento')]
    
    def on_button_click(documento_id):
        obtenerDocumentoDesdeServidor(documento_id)
        ventanaListar.destroy()
    
    for i, documento_id in enumerate(id_doc):
        button = tk.Button(ventanaListar, text=documento_id, command=lambda id=documento_id: on_button_click(id))
        button.configure(width=20, height=2) 
        button.place(relx=0.5, rely=(i+1)/(len(id_doc)+0.5), anchor="center")


def listarDesdeServidor():
    datos = {"accion": "listar"}
    datos = json.dumps(datos)
    return SocketCliente(datos)

def obtenerDocumentoDesdeServidor(documento_id):
    global nuevo, id
    datos = {"_id": documento_id, "accion": "obtener"}
    datos = json.dumps(datos)
    nuevo = False 
    id = documento_id
    SocketCliente(datos)
    


#Guardar el archivo cifrado en la BD MONGO    
def guardarEnServidor(ventana, nombreDocumento):
    global tipoCifrado
    global clave
    global nuevo, obtenido
    global id
    if nuevo == True:
        contenidoCifrado =  editorTexto.get("1.0", "end-1c")

        #Json
        datos = {"_id": nombreDocumento,
                "contenido": contenidoCifrado,
                "tipoCifrado": tipoCifrado,
                "clave" : clave,
                "accion": "guardar"}
        
        datos = json.dumps(datos)
        SocketCliente(datos)
        nuevo = False
        id = nombreDocumento
        ventana.destroy()
    elif nuevo == False:
        
        if tipoCifrado == "Monoalfabetico":
            obtenido=True
            cifradoMonoalfabetico()
        elif tipoCifrado == "Polialfabetico":
            obtenido=True
            cifradoPolialfabetico()
        contenidoCifrado =  editorTexto.get("1.0", "end-1c")
        datos = {"_id": id,
                "contenido": contenidoCifrado,
                "tipoCifrado": tipoCifrado,
                "clave" : clave,
                "accion": "actualizar"}
        
        datos = json.dumps(datos)
        SocketCliente(datos)
        ventana.destroy()

    
    
def SocketCliente(datosJson = None):

    config = configparser.ConfigParser()
    config.read('config.ini')
    Host = config.get('Settings', 'Host')
    Puerto = int(config.get('Settings', 'Puerto'))
    socketCliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        socketCliente.connect((Host, Puerto))
        socketCliente.sendall(datosJson.encode())
        respuesta = socketCliente.recv(1024).decode()
        datos = json.loads(datosJson)
        if datos["accion"] == "guardar" or datos["accion"] == "actualizar":
            messagebox.showinfo("Respuesta del servidor", respuesta)

        elif datos["accion"] == "obtener":
            # Procesar la respuesta XML
            global  clave, obtenido, tipoCifrado
            root = ElementTree.fromstring(respuesta)
            contenido = root.find("Contenido").text
            editorTexto.delete("1.0", tk.END)
            editorTexto.insert(tk.END, contenido)
            if root.find("TipoCifrado").text == "Monoalfabetico":
                clave = root.find("Clave").text
                obtenido=True
                tipoCifrado="Monoalfabetico"
                descifradoMonoalfabetico()
            elif root.find("TipoCifrado").text == "Polialfabetico":
                clave = root.find("Clave").text
                obtenido=True
                tipoCifrado="Polialfabetico"
                descifradoPolialfabetico()
            
        else:
             return respuesta
    except Exception as e:
        print(e)
    finally:
        socketCliente.close() 
       
#**********************************************************************        


#Ventana principal
ventanaPrincipal = tk.Tk()
ventanaPrincipal.title("Programa de Cifrado")
menuPrincipal = tk.Menu(ventanaPrincipal)
ventanaPrincipal.config(menu=menuPrincipal)
ventanaPrincipal.geometry('1000x750+300+40')
ventanaPrincipal.configure(background="CadetBlue") 

# Menu
#Archivo
menuArchivo = tk.Menu(menuPrincipal, tearoff=0)
menuArchivo.add_command(label="Abrir", command=abrirArchivo)
menuArchivo.add_command(label="Guardar", command=guardarArchivo)
menuArchivo.add_command(label="Guardar Como", command=guardarComoArchivo)
menuArchivo.add_command(label="Nuevo", command=nuevoArchivo)
menuArchivo.add_separator()
menuArchivo.add_command(label="Salir", command=salirAplicacion)
menuPrincipal.add_cascade(label="Archivo", menu=menuArchivo)


#Cifrado
menuCifrado = tk.Menu(menuPrincipal, tearoff=0)
menuCifrado.add_command(label="Cifrado Monoalfabetico", command=cifradoMonoalfabetico)
menuCifrado.add_command(label="Descifrado Monoalfabetico", command=descifradoMonoalfabetico)
menuCifrado.add_separator()
menuCifrado.add_command(label="Cifrado Polialfabetico", command=cifradoPolialfabetico)
menuCifrado.add_command(label="Descifrado Polialfabetico", command=descifradoPolialfabetico)
menuCifrado.add_separator()
menuCifrado.add_command(label="Guardar en el servidor", command=ventanaGuardarEnServidor)
menuCifrado.add_command(label="Abrir desde servidor", command=vetanaListarDesdeServidor)
menuPrincipal.add_cascade(label="Cifrado", menu=menuCifrado)


#Opciones
menuOpciones = tk.Menu(menuPrincipal, tearoff=0)
menuOpciones.add_command(label="Configuración", command=VentanaConfiguracion)
menuPrincipal.add_cascade(label="Opciones", menu=menuOpciones)


#Barra de herramientas
toolBar = tk.Frame(ventanaPrincipal)
toolBar.pack(side = "top", fill = "x")

#Copiar
imagenCopiar = Image.open("iconos\copiar.png")
imgCopiarAjustada = imagenCopiar.resize((30, 30), Image.LANCZOS)
imagenCopiarTk = ImageTk.PhotoImage(imgCopiarAjustada)
botonCopiar = tk.Button(toolBar, command=copiarTexto, image=imagenCopiarTk)
botonCopiar.pack(side="left", padx=2, pady=2)

#Pegar
imagenPegar = Image.open("iconos\pegar.png")
imgPegarAjustada = imagenPegar.resize((30, 30), Image.LANCZOS)
imagenPegarTk = ImageTk.PhotoImage(imgPegarAjustada)
botonPegar = tk.Button(toolBar, command=pegarTexto, image=imagenPegarTk)
botonPegar.pack(side="left", padx=2, pady=2)

#Cortar
imagenCortar = Image.open("iconos\cortar.png")
imgCortarAjustada = imagenCortar.resize((30, 30), Image.LANCZOS)
imagenCortarTk = ImageTk.PhotoImage(imgCortarAjustada)
botonCortar = tk.Button(toolBar, command=cortarTexto, image=imagenCortarTk)
botonCortar.pack(side="left", padx=2, pady=2)


#Editor de texto
editorTexto = tk.Text(ventanaPrincipal, wrap="word", width=200, height=100, bd=5, relief=tk.GROOVE)
editorTexto.pack(padx=10, pady=10)


ventanaPrincipal.mainloop()
