#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse


class Profesor(Resource):

    def get(self, _id):
        profesor = ProfesorModel.buscar_por_id(_id)
        if profesor:
            return profesor.obtener_datos()
        return {'mensaje': 'No se encontró el recurso solicitado'}, 404

    def delete(self, _id):
        profesor = ProfesorModel.buscar_por_id(_id)
        if profesor:
            try:
                profesor.eliminar()
                return {'message': 'profesor eliminado con éxito'}
            except Exception as e:
                return {'message': 'No se pudo realizar la eliminación'}, 500
        else :
            return {'mensaje': 'No se encontró el recurso solicitado'}, 404



class Profesores(Resource):

    # PARSER: se pueden definir los argumentos que DEBEN o PUEDEN venir como parámetros en la llamada
    # Puede verse un poco feo para tablas con muchos campos y resultar algo tedioso pero tiene un beneficio
    # Podemos controlar la información que nos mandan (tipo de datos, rango de valores, etc).
    # Además, si se añade a la fuerza un parámetro indeseadoeste filtro lo elimina.
    # Ojo: Este modelo tiene el campo 'fecha_inscripcion'. No lo defino como argumento en el parser request.
    # por lo que, aunque le mandemos ese parámetro y exista en la base de datos, lo desechará igualmente.
    # Acá nos funciona porque en BD tiene un default NOW() pero si usamos el filtro debemos añadir todos los parámetros necesarios.
    parser = reqparse.RequestParser()
    parser.add_argument('nombres',
        type=str,
        required=True,
        help="Debe ingresar un nombre para el profesor"
    )
    parser.add_argument('apellidos',
        type=str,
        required=True,
        help="Debe ingresar un apellido para el profesor."
    )
    parser.add_argument('activo',
        type=int,
        required=False,
        choices=(0, 1),
        help="Debe ingresar 0 para estado inactivo y 1 para estado activo."
    )


    def get(self):
        return {'Profesores': list(map(lambda x: x.obtener_datos(), ProfesorModel.query.all()))}


    def post(self):
        data = Profesores.parser.parse_args()
        if ProfesorModel.buscar_existencia(data['nombres'],data['apellidos']):
            return {'message': "Ya existe un profesor llamado '{} {}'. Uno es suficiente!".format(data['nombres'], data['apellidos'])}, 400
        profesor = ProfesorModel(data['nombres'],data['apellidos'])
        profesor.activo = data['activo'] if data['activo'] else None
        try:
            profesor.guardar()
        except:
            return {"message": "No se pudo resolver su petición."}, 500
        return profesor.obtener_datos(), 201

    # La acción PUT ingresa un recurso en caso de que no exista. Si existe actualiza todos los valores
    def put(self):
        data = Profesores.parser.parse_args()
        if ProfesorModel.buscar_existencia(data['nombres'],data['apellidos']):
            profesor = ProfesorModel.buscar_existencia(data['nombres'],data['apellidos'])
        else :
            profesor = ProfesorModel(data['nombres'],data['apellidos'])

        profesor.activo = data['activo'] if data['activo'] else None

        try:
            profesor.guardar()
        except:
            return {"message": "No se pudo resolver su petición."}, 500
        return profesor.obtener_datos(), 201

class CursosProfesor(Resource):

    def get(self, _id):
        profesor = ProfesorModel.buscar_por_id(_id)
        if profesor:
            cursos = profesor.cursos
            listaCursos = {}
            for curso in cursos:
                listaCursos[curso.id] = {"nombre":curso.nombre,"nivel":curso.nivel}
            dataProfesor = profesor.obtener_datos()
            dataProfesor['cursos'] = listaCursos
            return dataProfesor
        return {'mensaje': 'No se encontró el recurso solicitado'}, 404
