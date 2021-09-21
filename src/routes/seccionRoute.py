from src.controllers.seccionController import SeccionController
from src import app
from flask import json, request, session, Response, jsonify
from src.models.seccion import Seccion 
from src.dto.seccion import SeccionDTO 

seccionController = SeccionController()

@app.route('/seccion', methods=['POST'])
def crear_seccion():
    if request.method=='POST':
        nombre=request.form["nombre"]
        id_encuesta=request.form["id_encuesta"]

        seccionDto=SeccionDTO(
            nombre=nombre,
	        encuesta_id=id_encuesta
        )
        crearSeccion=seccionController.create(seccionDto)
    
        return Response('seccion base creada correctamente', 201, mimetype='application/json')

@app.route('/seccion')
def obtener_seccion():
    id_=request.args.get('id_')
    seccion=seccionController.get(int(id_))
    if(seccion):
        return jsonify(Seccion.json(seccion))
    else:
        return Response('No existe la seccion', 400, mimetype='application/json')
    
@app.route('/secciones', methods=['POST'])
def obtener_por_encuesta():
    if request.method=='POST':
        id_encuesta=request.form["id_encuesta"]
        seccions=seccionController.findByEncuesta(int(id_encuesta))
        return jsonify([Seccion.json(sec) for sec in seccions])


@app.route('/secciones')
def obtener_todas_las_sesiones():
    seccions=seccionController.list()
    return jsonify([Seccion.json(sec) for sec in seccions])

@app.route('/seccion',methods=['PUT'])
def actualizar_seccion():
    if request.method=='PUT':
        id_=request.form['id']
        nombre=request.form['nombre']
        seccionController.update(int(id_),nombre)
        response = Response("seccion Actualizada", 201, mimetype='application/json')
        return response       

@app.route('/seccion',methods=['DELETE'])
def eliminar_seccion():
    if request.method=='DELETE':
        id_=request.form["id"]
        seccionController.delete(int(id_))
        response = Response("seccion eliminada", 201, mimetype='application/json')
        return response  




