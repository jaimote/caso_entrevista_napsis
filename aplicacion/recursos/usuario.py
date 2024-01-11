#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from aplicacion.modelos.usuario import UsuarioModel

class Usuario(Resource):

    def get(self, _id):
        """
            @apiGroup Usuario
            @apiName Buscar usuario
            @api {get} /usuario/:id
            @apiVersion 1.0.0
            @apiDescription Busca un usuario por su id
            @apiExample {json} Example-Response:
                {
                    "id": 1,
                    "username": "Florencia",
                    "apellidos": "Padilla",
                    "fecha_inscripcion": "25-03-2018",
                    "activo": true
                }
        """
        usuario = UsuarioModel.buscar_por_id(_id)
        if usuario:
            return usuario.obtener_datos()
        return {'mensaje': 'No se encontró el recurso solicitado'}, 404

    def delete(self, _id):
        usuario = UsuarioModel.buscar_por_id(_id)
        if usuario:
            try:
                usuario.eliminar()
                return {'message': 'Usuario eliminado con éxito'}
            except Exception as e:
                return {'message': 'No se pudo realizar la eliminación'}, 500
        else :
            return {'mensaje': 'No se encontró el recurso solicitado'}, 404



class Usuarios(Resource):

    # PARSER: se pueden definir los argumentos que DEBEN o PUEDEN venir como parámetros en la llamada
    # Puede verse un poco feo para tablas con muchos campos y resultar algo tedioso pero tiene un beneficio
    # Podemos controlar la información que nos mandan (tipo de datos, rango de valores, etc).
    # Además, si se añade a la fuerza un parámetro indeseadoeste filtro lo elimina.
    # Ojo: Este modelo tiene el campo 'fecha_inscripcion'. No lo defino como argumento en el parser request.
    # por lo que, aunque le mandemos ese parámetro y exista en la base de datos, lo desechará igualmente.
    # Acá nos funciona porque en BD tiene un default NOW() pero si usamos el filtro debemos añadir todos los parámetros necesarios.
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="Debe ingresar un nombre para el usuario"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="Debe ingresar una password para el usuario"
    )
    parser.add_argument('salt',
        type=str,
        required=True,
        help="Debe ingresar salt para el usuario"
    )
    parser.add_argument('activo',
        type=int,
        required=False,
        choices=(0, 1),
        help="Debe ingresar 0 para estado inactivo y 1 para estado activo."
    )

    def get(self):
        return {'usuarios': list(map(lambda x: x.obtener_datos(), UsuarioModel.query.all()))}

    def post(self):
        data = Usuarios.parser.parse_args()
        if UsuarioModel.buscar_username(data['username']):
            return {'message': "Ya existe un usuario llamado '{}'. Uno es suficiente!".format(data['username'])}, 400
        usuario = UsuarioModel(data['username'],data['password'])
        usuario.salt = data['salt'] if data['salt'] else None
        usuario.activo = data['activo'] if data['activo'] else None
        try:
            usuario.guardar()
        except:
            return {"message": "No se pudo resolver su petición."}, 500
        return usuario.obtener_datos(), 201

    # La acción PUT ingresa un recurso en caso de que no exista. Si existe actualiza todos los valores
    def put(self):
        data = Usuarios.parser.parse_args()
        if UsuarioModel.buscar_username(data['username']):
            usuario = UsuarioModel.buscar_username(data['username'])
        else :
            usuario = UsuarioModel(data['username'],data['password'])

        usuario.activo = data['activo'] if data['activo'] else None

        try:
            usuario.guardar()
        except:
            return {"message": "No se pudo resolver su petición."}, 500
        return usuario.obtener_datos(), 201
