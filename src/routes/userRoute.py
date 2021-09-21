#controlador, #app, flask, response,dto, 
from src.controllers.auth.userController import UserController
from src import app
from flask import request, session, Response 
from src.models.user import User
from src.dto.user import UserDTO
import hashlib

userController = UserController()

@app.route('/register', methods=['POST'])
def registrar_usuario():
    validation=''
    if request.method=='POST':
        nombre=request.form["nombre"]
        email=request.form["email"]
        contrasenia=request.form["contrasenia"]

    if(userController.userFound(nombre)):
            validation="El nombre de usuario ya existe en la base de datos, elige otro porfavor"
            return Response(validation, 400, mimetype='application/json')
    else:
        validation="Usuario creado, Puedes Iniciar Sesion"
        #contrasenia encryptada
        h=hashlib.new("sha1",str(contrasenia).encode('utf-8'))
        password=h.hexdigest()
        #agregamos el nuevo usuario a la base de datos
        userDto=UserDTO(
            nombre=nombre,
            email=email,
            contrasenia=password
        )
        crearUsuario=userController.create(userDto)
        return Response(validation, 201, mimetype='application/json')

@app.route('/login', methods=['POST'])
def iniciar_sesion():
    validation=""
    if(request.method=="POST"):
        nombre=request.form.get('nombre')
        contrasenia=request.form.get('contrasenia')

        #filtrar por nombre y contrasenia en la db
        h=hashlib.new("sha1",str(contrasenia).encode('utf-8'))
        password=h.hexdigest()

        userdto=UserDTO(nombre,"",password)
        resolve_user=userController.authUser(userdto)

        if(resolve_user):
            session.permanent=True
            session["user"]=resolve_user.nombre
            session["id"]=resolve_user.id
            validation='sesion iniciada correctamente'
            return Response(validation, 201, mimetype='application/json')

        else:
            validation="Nombre de usuario o contraseña incorrectos"
            return Response(validation, 400, mimetype='application/json')


@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("id",None)
    return Response('sesion cerrada correctamente', 201, mimetype='application/json')

@app.route('/auth')
def auth():
    if "user" in session:
        user=session["user"]
        return Response(user, 201, mimetype='application/json')
    return Response("No hay un usuario en la sesion", 400, mimetype='application/json')
