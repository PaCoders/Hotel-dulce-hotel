from bottle import run, request, response, get, post, put, error, delete, abort
import os, json

bd = [] #Aqui se guardan todas las habitaciones

class Room: #Clase objeto
    def __init__(self, id_h, plazas, list_equipo, ocup):
        self.id = id_h
        self.plazas = plazas
        self.list_equipo = list_equipo
        self.ocup = ocup

def cargarBD(): #Cargar la base de datos

    global bd

    if len(bd) > 0: #Si hay elementos en la BD, entonces no necesitamos cargar nada
        return

    check = os.path.isfile("habitaciones.txt") #Comprobamos que el fichero exista

    if check == True:
        f = open("habitaciones.txt")
        for dor in f: #Guardamos las habitaciones que estan en el fichero en una lista global simulando una BD
            dorm = dor.rstrip("\n") #Quitamos el salto de linea del final
            hab = eval(dorm)
            id_r = int(hab["id"])
            lista = list(hab["list_equip"])
            h = Room(id_r,int(hab["aforo"]),lista,str(hab["ocup"])) #Guardamos los atributos de la habitacion en un objeto
            bd.append(h) #Guardamos dicho objeto en la base de datos
        f.close()
    else:
        return #Si no hay archivos, entonces salimos de la funcion

def guardarHabitaciones(plazas,lista,ocupa): #Guardar habitacion en el fichero

    cargarBD() #Cargamos la BD
        
    id_habitacion = 1
   
    for dorm in bd: #Comprobamos las ID que ya estan asignadas
        if id_habitacion == dorm.id:
            id_habitacion += 1

    h = Room(id_habitacion,plazas,lista,ocupa) #Guardamos los datos de este en un objeto

    bd.append(h) #Introducimos el objeto en la BD
    arch = open("habitaciones.txt","a") #Guardamos estos datos en el fichero
    string = "{'id':"+ str(id_habitacion)+",'aforo':"+str(plazas)+",'list_equip':"+str(lista)+",'ocup':'"+str(ocupa)+"'}\n"
    arch.write(string)
    arch.close()
    return id_habitacion

@post("/alta")
def darAlta(): #Aqui obtenemos los datos y los deberiamos guardar en un json
    data = request.json
    values = json.loads(data)
    
    aforo = int(values.get("aforo"))
    lista = values.get("list_equip")
    ocupa = values.get("ocup")

    #Segundo metemos los datos que hemos recibido en la lista

    id_asig = guardarHabitaciones(aforo,lista,ocupa)

    response.headers["Content-Type"] = "application/json"

    toJson = {"id": id_asig, "aforo":aforo, "list_equip":lista, "ocup":ocupa}
    return json.dumps(toJson) #Devolvemos un json de respuesta para que sepa el cliente que los datos se han almacenado correctamente


@post("/modificar/<id_u>")
def modificarHabitacion(id_u):
    id_h = int(id_u)
    cargarBD()

    check = False #No existe ninguna habitacion con dicho ID

    for dorm in bd:
        if id_h == dorm.id: #Comprobamos que exista una habitacion con dicha ID
            check = True
            break
    
    if check == True:
        data = request.json #Obtenemos el json enviado por el cliente
        value = json.loads(data) #Pasamos el json a diccionario
        
        h = Room(id_h, int(value["aforo"]),value["list_equip"],value["ocup"])

        for cont in range(0,len(bd)): #Buscamos la habitacion
            if bd[cont].id == id_h:
                bd.pop(cont) #Eliminamos la habitación de la lista
                bd.insert(cont, h) #Introducimos la habitación ya modificada
                break
        
        a = open("habitaciones.txt","w") #Sobreescribimos el fichero
        for room in bd:
            string = "{'id':"+ str(room.id)+",'aforo':"+str(room.plazas)+",'list_equip':"+str(room.list_equipo)+",'ocup': '"+str(room.ocup)+"'}\n"
            a.write(string)
        a.close()
    else:
        abort(404, "No se ha encontrado el elemento con la ID indicada.")

@post("/ocupacion/<ocupa>")
def modificarOcupacion(ocupa):

    cargarBD() #Cargamos la BD en caso de que fuese necesario
        
    ocupacion = []
    format_json = {}
    for dat in bd:
        if dat.ocup == ocupa:
            format_json = {"id": dat.id, "aforo":dat.plazas, "list_equip":dat.list_equipo}
            ocupacion.append(format_json)
    
    if len(ocupacion) == 0: #Si no existe ningun elemento del buscado pues es que no hay ninguna habitacion con la condicion dada
        abort(404, "No se ha encontrado ningun elemento con la ocupacion dada.")
        return
    
    response.headers["Content-Type"] = "application/json"
    json_parse = json.dumps(ocupacion)
    return json_parse 
    

@get("/consulta/completa")# Devuelve los datos de todas las Habitaciones del Hotel
def ConsCompleta():

    listado = [] # Lista donde guardaremos las Habitaciones

    cargarBD() # Cargamos los datos de las habitaciones a partir de una función ya definida

    for value in bd:   # Metemos los valores del diccionario en la lista que previamente creamos
        listado.append({"id": value.id, "aforo":value.plazas, "list_equip":value.list_equipo,"ocup":value.ocup})

    response.headers["Content-Type"] = "application/json"
    json_parse = json.dumps(listado)
    return json_parse  


@post("/consulta/seleccion/<id_u>")
def ConsSeleccion(id_u):
    id = int(id_u)
    room_aux = {}

    cargarBD()

    check = False

    for value in bd:      # Buscamos la Habitación
        if id == value.id:  # Guardamos los valores de la habitación que coincida con la ID
            room_aux = {"id": value.id, "aforo":value.plazas, "list_equip":value.list_equipo,"ocup":value.ocup}
            check = True
            break

    if check == False:
        abort(404, "Perdone pero no se encuentra el elemento que busca disponible.")

    response.headers["Content-Type"] = "application/json"
    json_parse = json.dumps(room_aux)
    return json_parse   

@delete("/borrar/<id_u>")
def borrarHabitacion(id_u):

    id = int(id_u)
    cargarBD()
    
    check = False
    
    for i in range(0,len(bd)):
        if bd[i].id == id: #Buscamos el elemento solicitado para eliminarlo de BD
            bd.pop(i)
            check = True
            break
    
    if check == False:
        abort(404, "Perdone pero no se encuentra el elemento que busca disponible.")
        return

    id_habitacion = 1
   
    for i in range(0, len(bd)): #Reasignamos las ID
        if bd[i].id != id_habitacion:
            bd[i].id = id_habitacion
        else:
            id_habitacion += 1

    f = open("habitaciones.txt","w") #Sobreescribimos el fichero
    for room in bd:
        string = "{'id':"+ str(room.id)+",'aforo':"+str(room.plazas)+",'list_equip':"+str(room.list_equipo)+",'ocup':'"+str(room.ocup)+"'}\n"
        f.write(string)
    f.close()
   
if __name__ == "__main__":  
    run(host="localhost", port=8080, debug=True)