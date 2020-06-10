import json, requests

#-------- FUNCIONES --------

def darAlta(): 

    while True: #Vamos a registrar las habitaciones
        habitacion = dict() #Creamos un diccionario vacio de la habitacion a enviar al servicio

        while True:
            aforo = int(input(">>Aforo de la habitación: "))
            if aforo > 0 and aforo < 7: #El aforo mínimo es 1 persona y el máximo 6
                break
            print(">>Vuelva a introducir el aforo por favor.\n")
        habitacion["aforo"] = aforo

        obj = input(">>Introduzca la lista de equipamiento: ") #Introducimos los objetos disponibles en la habitacion

        space = False
        for eq in obj: #Comprobamos si tiene espacio lo introducido por teclado para que quede igual que los de la BD del servicio
            if eq == " ":
                space = True
        
        if space == False: 
            equip = obj.split(",")
        else:
            equip = obj.split(", ")
        
        habitacion["list_equip"]= equip

        while True:
            ocup = input(">>¿Está la habitación ocupada? (Sí/No).")
            if (ocup == "Si" or ocup == "si" or ocup == "Sí" or ocup == "SI") or (ocup == "No" or ocup == "no" or ocup == "NO"):
                break

        if ocup == "SI" or ocup == "si" or ocup == "Sí":
            ocup = "Si"

        elif ocup == "NO" or ocup == "no":
            ocup = "No"
        habitacion["ocup"] = ocup

        toServer = json.dumps(habitacion)
        try:
            res = requests.post("http://localhost:8080/alta", json=toServer) #Enviamos la habitacion al servidor del servicio
            rec = res.json() #Recibimos un json por parte del servicio como si fuera un recibo de que se ha guardado correctamente nuestra habitacion
            print(">> Habitación dada de alta: \n")
            print(rec)

        except requests.exceptions.HTTPError:
            print("Se ha producido un error a la hora de comunicar con el servicio.\n")
        
        opc = int(input(">>¿Deseas introducir más habitaciones? Si es así, introduzca 1. "))
        
        if opc != 1:
            break

def modificarDatos():
    url_mod = "http://localhost:8080/modificar/"
    
    id_room = input(">>Introduzca la ID de la habitación que deseas modificar: ")
    url = url_mod + id_room #Introducimos la ID y la concatenamos con la URL que tenemos para acceder a dicha habitacion

    habitacion = dict() #A partir de aqui seguimos igual que la funcion de dar de alta una habitacion

    while True:
        aforo = int(input(">>Aforo de la habitación: "))
        if aforo > 0 and aforo < 7: #El aforo mínimo es 1 persona y el máximo 6
            break
        print(">>Vuelva a introducir el aforo por favor.\n")
    habitacion["aforo"] = aforo

    obj = input(">>Introduzca la lista de equipamiento: ")

    space = False
    for eq in obj:
        if eq == " ":
           space = True
        
    if space == False:
        equip = obj.split(",")
    else:
        equip = obj.split(", ")
        
    habitacion["list_equip"]= equip

    while True:
        ocup = input(">>¿Está la habitación ocupada? (Sí/No).")
        if (ocup == "Si" or ocup == "si" or ocup == "SI") or (ocup == "No" or ocup == "no" or ocup == "NO"):
           break

    if ocup == "SI" or ocup == "si":
        ocup = "Si"

    elif ocup == "NO" or ocup == "no":
        ocup = "No"
    habitacion["ocup"] = ocup

    room = json.dumps(habitacion)
    
    resp = requests.post(url,json=room)

    if resp.status_code == 404: #Si no se ha encontrado, el servicio nos envia este codigo de error
        print("No se ha encontrado dicha habitación.\n")
        return

    print("Habitacion con ID: "+id_room+", modificada correctamente.\n")
    
def ConsultaSeleccion(): #Funcion para consultar los datos de una habitacion mediante la ID
    url_mod = "http://localhost:8080/consulta/seleccion/"

    id_aux = input("Introduzca la ID de la Habitación a consultar: ")
    
    url = url_mod + id_aux

    resp = requests.post(url)  # Le enviamos al servicio la ID

    if resp.status_code == 404:
        print("No se ha encontrado ninguna habitacion con dicho ID.\n")
        return
        
    room = resp.json() #Recibimos el json con los datos de la habitacion
    print("\n------------------------------\n")
    print("\n>> ID:" + str(room["id"]) + "\n")
    print(">> Capacidad: " + str(room["aforo"]) + "\n")
    print(">> Lista de equipamiento:\n")
    for obj in room["list_equip"]:
        print("     - "+obj+"\n")
    print(">> ¿Ocupada?: "+room["ocup"]+"\n")
    print("------------------------------\n")


def ConsultaCompleta():
    url = "http://localhost:8080/consulta/completa"
    
    data = requests.get(url).json() #Recibimos el json de los datos de la habitacion

    #En este caso no hemos comprobado el codigo que recibimos ya que no vamos a buscar una habitacion concreta

    for room in data:
        print("\n------------------------------\n")
        print("\n>> ID:" + str(room["id"]) + "\n")
        print(">> Capacidad: " + str(room["aforo"]) + "\n")
        print(">> Lista de equipamiento:\n")
        for obj in room["list_equip"]:
            print("     - "+obj+"\n")
        print(">> ¿Ocupada?: "+room["ocup"]+"\n")
        print("------------------------------\n")
            
        
def consultarDisp():
    url_mod = "http://localhost:8080/ocupacion/"
    
    disp = input(">>¿Qué habitaciones deseas ver?: (Ocupada/Libre)")

    if disp == "Ocupada" or disp == "ocupada" or disp == "Ocupado" or disp == "ocupado":
        disp = "Si"

    if disp == "Libre" or disp == "libre":
        disp = "No"
    url = url_mod + disp

    resp = requests.post(url)

    if resp.status_code == 404:
        print("No se ha encontrado dicha habitación.\n")
        return

    for room in resp.json():
        print("\n------------------------------\n")
        print("\n>> ID:" + str(room["id"]) + "\n")
        print(">> Capacidad: " + str(room["aforo"]) + "\n")
        print(">> Lista de equipamiento:\n")
        for obj in room["list_equip"]:
            print("     - "+obj+"\n")
        print("------------------------------\n")

def borrarHabitacion():
    url_mod = "http://localhost:8080/borrar/"

    ConsultaCompleta() #Primero obtenemos la lista de todos los elementos para seleccionar
                            
    id = input(">>¿Qué habitaciones deseas eliminar?: (Introduzca el ID)")

    url = url_mod+id

    resp = requests.delete(url)

    if resp.status_code == 404:
        print("No se ha encontrado dicha habitación.\n")
        return
    
    print("Se ha eliminado la habitación: "+id+", correctamente.\n")
        
#-------- PROGRAMA PRINCIPAL --------

if __name__ == "__main__":

    while True: #Menu del cliente
        print("MENU: \n")
        print("--- 1. Dar de alta una nueva habitación. ---\n")
        print("--- 2. Modificar los datos de una habitación. ---\n")
        print("--- 3. Consultar Habitación. ---\n")
        print("--- 4. Consultar habitaciones ocupadas o desocupadas. ---\n")
        print("--- 5. Borrar habitacion. ---\n")
        print("--- Para salir, introduzca 0. ---\n")
        men = int(input("OPCIÓN:"))

        if men == 0:
            break
        elif men == 1:
            darAlta()
        elif men == 2:
            modificarDatos()
        elif men == 3: #En esta opcion del menu nos da dos opciones de consulta
            print("Selecciona Método de Consulta.\n")  
            print("--- 1. Consulta Completa de Habitaciones del Hotel. ---\n") 
            print("--- 2. Consulta a partir de una ID. ---\n")
            men2 = int(input("OPCIÓN: "))
            if men2 == 1:
                ConsultaCompleta()
            elif men2 == 2:
                ConsultaSeleccion()
        elif men == 4:
            consultarDisp()
        elif men == 5:
            borrarHabitacion()

         