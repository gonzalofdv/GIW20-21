"""
GIW 2020-21
Práctica 7
Grupo 2
Autores: Jin Wang Xu, Jorge Borja García, Fernando González Zamorano, Gonzalo Figueroa del Val

Jin Wang Xu, Jorge Borja García, Fernando González Zamorano y Gonzalo Figueroa del Val declaramos que esta solución es fruto exclusivamente
de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
"""
from flask import Flask, request, session, render_template
app = Flask(__name__)

id = 0
asignaturas = list()

def comprobarDict(asignaturaJSON):
    ok = False
    if "nombre" in asignaturaJSON and "numero_alumnos" in asignaturaJSON and "horario" in asignaturaJSON and len(asignaturaJSON.keys()) == 3: #Fase 1 Debe contener 3 campos 
        if(type(asignaturaJSON["nombre"]) is str and type(asignaturaJSON["numero_alumnos"]) is int and type(asignaturaJSON["horario"]) is list): #Fase 2 Los 3 campos deben ser de tipo, str, int y list respectivamente
            ok = True # En este punto, ya es True, si toda la estructura de horario es correcto. Puede contener 0, 1 o varios horarios 
            for horario in asignaturaJSON["horario"]: #Para cada horario dentro de la lista | Tener en cuenta que si hay 0 horarios, no se ejecuta el foreach y ok = True
                if(type(horario) is dict): #Fase 3 Debe contener uno o varios diccionarios
                    if("dia" in horario and "hora_inicio" in horario and "hora_final" in horario and len(horario.keys()) == 3 ): #Fase 4 Debe contener 3 campos
                        if(type(horario["dia"]) is str and type(horario["hora_inicio"]) is int and type(horario["hora_final"]) is int): #Fase Final Los 3 campos deben de ser de tipo str e int
                            ok = True
                        else: #Si en caso de que haya un horario que no
                            ok =False 
                            break # Un break para que deje de recorrer el foreach
                    else:
                        ok = False
                        break
                else:
                    ok = False
                    break

    return ok

@app.route('/asignaturas', methods=['DELETE'])
def borrarAsignaturas():
    asignaturas.clear() #Borra todo contenido de la lista global de asignaturas
    global id 
    id = 0 # El contador global vuelve a 0
    return "NO CONTENT", 204


@app.route('/asignaturas', methods=['GET'])
def listaAsignatura():
    #Lo primero de todo, recoge los parametros, si no existe un parametro, le asigna el valor "None" o 0 si el parametro es el nº de alumnos
    pagina = request.args.get("page", "None")
    numeros = request.args.get("per_page", "None")  
    alumnosGTE = request.args.get("alumnos_gte", 0)
    STATUS = 200
    listaURL = list()
    jsonAsignaturas = ""
    if(pagina == "None" and numeros != "None" or pagina != "None" and numeros == "None"): #Para saber si los dos parametros page y per_page estan definidos, si no lo estan el estado es 400
        STATUS = 400
    else:
        if(len(asignaturas) != 0): #Si no hay ninguna asignatura, devolvera una lista vacia 

            #Primero filtramos el numero de alumnos
            for asignatura in asignaturas:
                if(asignatura["numero_alumnos"] >= int(alumnosGTE)):
                    URL = "/asignaturas/" + str(asignatura["id"])
                    listaURL.append(URL)
                else: #Si el filtrado de alumnos funciona y descarta una URL, el STATUS será 206
                    STATUS = 206
            #Se realiza el paginado tras filtrar el numero de alumnos
            if(pagina != "None" and numeros != "None" ): 
                listaAux = list()
                puntero = 0 #contador que sirve para recorrer todos los URLs ya filtrados con el nº de Alumnos, para paginar los URLs
                for i in range(int(pagina)):
                    for j in range(int(numeros)):
                        if(puntero == len(listaURL)): #Si el puntero recorre hasta el final de la lista, hace un break para salir del bucle
                            break
                        if(i + 1 == int(pagina)): #Si coincide la iteracion i con el numero de la pagina del parametro, empezará a insertar las URL en esa pagina
                            listaAux.append(listaURL[puntero])
                        puntero = puntero + 1
                if(len(listaAux) < len(listaURL)):
                    STATUS = 206
                listaURL = listaAux
    jsonAsignaturas = {"asignaturas" : listaURL}

    return jsonAsignaturas, STATUS

@app.route('/asignaturas', methods=['POST'])
def crearAsignatura():
    asignaturaJSON = request.json
    ret = ""
    STATUS = 400
    if(comprobarDict(asignaturaJSON)): #Comprueba su el esquema del JSON Asignatura es correcta
        STATUS = 201
        global id 
        id = id + 1
        ret = {'id' : id}
        asignaturaJSON['id'] = id
        asignaturas.append(asignaturaJSON) #Si lo es, inserta en la lista global de asignaturas y agrega un campo ID

    return ret, STATUS

@app.route('/asignaturas/<int:numId>', methods=['GET'])
def mostrarAsignatura(numId):
    STATUS = 404
    resultado = {}
    for asignatura in asignaturas:
        if(asignatura["id"] == numId):
            STATUS = 200
            resultado = asignatura

    return resultado, STATUS

@app.route('/asignaturas/<int:numId>', methods=['PUT'])
def actualizarAsignatura(numId):
    STATUS = 404
    asignaturaJSON = request.json
    i = 0 #Contador para recorrer la lista global de asignaturas
    for asignatura in asignaturas:
        if(asignatura["id"] == numId):
            STATUS = 200
            if(comprobarDict(asignaturaJSON)):
                asignaturaJSON["id"] = numId #Agrega el ID 
                asignaturas[i] = asignaturaJSON #Y sustituye al diccionario anterior por la nueva
            else:
                STATUS = 400
        i = i + 1

    return "", STATUS

@app.route('/asignaturas/<int:numId>', methods=['PATCH'])
def actualizarCampo(numId):
    STATUS = 404
    campoJSON = request.json
    i = 0 #Contador para recorrer la lista global de asignaturas
    if(len(campoJSON.keys()) != 1): #Significa que ha pasado un json de longitud no valida 
        STATUS = 400
    else:
        clave = list(campoJSON.keys())[0]
        valor = list(campoJSON.values())[0]
        for asignatura in asignaturas:
            if(asignatura["id"] == numId):
                aux = asignatura.copy() #Guarda el diccionario con el ID coincidente 
                aux[clave] = valor #Sustituye el nuevo campo con el viejo en el diccionario auxiliar
                idAsig = aux.pop("id") #Borra el campo ID para pasar la comprobacion del esquema del JSON Asignatura
                if(comprobarDict(aux)):
                    STATUS = 200
                    asignatura[clave] = valor #Si todo va bien ya podemos introducir el nuevo valor
                    asignaturas[i] = asignatura
                else: #Si falla, hay que volver a introducir el ID que habíamos eliminado
                    STATUS = 400
        i = i + 1

    return "", STATUS

@app.route('/asignaturas/<int:numId>', methods=['DELETE'])
def borrarAsignatura(numId):
    STATUS = 404
    i = 0 #Contador para recorrer la lista global de asignaturas
    for asignatura in asignaturas:
        if(asignatura["id"] == numId):
            STATUS = 204
            asignaturas.pop(i) #Borra el diccionario donde coincida el campo ID

        i = i + 1

    return "", STATUS

@app.route('/asignaturas/<int:numId>/horario', methods=['GET'])
def consultarHorario(numId):
    STATUS = 404
    horario = {}
    for asignatura in asignaturas:
        if(asignatura["id"] == numId):
            STATUS = 200
            horario = {"horario": asignatura["horario"]} #Crea un diccionario con campo Horario y el valor, la lista de horarios

    return horario, STATUS

class FlaskConfig:
    """Configuración de Flask"""
    # Activa depurador y recarga automáticamente 
    ENV = 'development'
    DEBUG = True
    TEST = True
    # Imprescindible para usar sesiones
    SECRET_KEY = "giw2020&!_()"
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


if __name__ == '__main__':
    app.config.from_object(FlaskConfig())
    app.run()