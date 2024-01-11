#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from aplicacion.modelos.curso import CursoModel
from aplicacion.modelos.profesor import ProfesorModel

class Curso(Resource):

    # PARSER: se pueden definir los argumentos que DEBEN o PUEDEN venir como parámetros en la llamada
    # Puede verse un poco feo para tablas con muchos campos y resultar algo tedioso pero tiene un beneficio
    # Podemos controlar la información que nos mandan (tipo de datos, rango de valores, etc).
    # Además, si se añade a la fuerza un parámetro indeseadoeste filtro lo elimina.
    # Ojo: Este modelo tiene el campo 'fecha_inscripcion'. No lo defino como argumento en el parser request.
    # por lo que, aunque le mandemos ese parámetro y exista en la base de datos, lo desechará igualmente.
    # Acá nos funciona porque en BD tiene un default NOW() pero si usamos el filtro debemos añadir todos los parámetros necesarios.
    parser = reqparse.RequestParser()
    parser.add_argument('nombre',
        type=str,
        required=True,
        help="Debe ingresar un nombre para el curso"
    )
    parser.add_argument('id_profesor',
        type=int,
        required=True,
        help="Debe ingresar el identificador del profesor que dictará el curso."
    )
    parser.add_argument('nivel',
        type=int,
        required=True,
        choices=(1, 2, 3, 4),
        help="Debe ingresar el nivel (entero del 1 al 4)."
    )
    parser.add_argument('activo',
        type=int,
        required=False,
        choices=(0, 1),
        help="Debe ingresar 0 para estado inactivo y 1 para estado activo."
    )

    def get(self, _id):
        curso = CursoModel.buscar_por_id(_id)
        if curso:
            return curso.obtener_datos()
        return {'mensaje': 'No se encontró el recurso solicitado'}, 404

    def delete(self, _id):
        curso = CursoModel.buscar_por_id(_id)
        if curso:
            try:
                curso.eliminar()
                return {'message': 'Curso eliminado con éxito'}
            except Exception as e:
                return {'message': 'No se pudo realizar la eliminación'}, 500
        else :
            return {'mensaje': 'No se encontró el recurso solicitado'}, 404


    def put(self, _id):
        data = Cursos.parser.parse_args()
        if CursoModel.buscar_por_id(_id):
            if ProfesorModel.buscar_por_id(data['id_profesor']):
                curso = CursoModel.buscar_por_id(_id)
                curso.nombre = data['nombre']
                curso.id_profesor = data['id_profesor']
                curso.nivel = data['nivel']
                curso.activo = data['activo'] if data['activo'] else None
                curso.activo = data['activo'] == 0 if data['activo'] else None
                try:
                    curso.guardar()
                except:
                    return {"message": "No se pudo resolver su petición."}, 500
                return curso.obtener_datos(), 201
            else :
                return {'message': "El identificador del profesor ingresado no es válido"}, 400
        else :
            return {'message': "No se encontró el curso"}, 404


class Cursos(Resource):

    # COPIÉ Y PEGUÉ LAS VALIDACIONES DE LA CLASE DE ARRIBA
    # TAL VEZ SE PODRÍA UTILIZAR HERENCIA DE CLASES PARA NO TENER QUE TIPIARLAS
    # DE NUEVO, AUNQUE LA FILOSOFÍA DE ESTO ES QUE CADA RECURSO SEA INDEPENDIENTE
    # DE OTRO AUNQUE TENGAN CARACTERÍSTICAS SIMILARES
    parser = reqparse.RequestParser()
    parser.add_argument('nombre',
        type=str,
        required=True,
        help="Debe ingresar un nombre para el curso"
    )
    parser.add_argument('id_profesor',
        type=int,
        required=True,
        help="Debe ingresar el identificador del profesor que dictará el curso."
    )
    parser.add_argument('nivel',
        type=int,
        required=True,
        choices=(1, 2, 3, 4),
        help="Debe ingresar el nivel (entero del 1 al 4)."
    )
    parser.add_argument('activo',
        type=int,
        required=False,
        choices=(0, 1),
        help="Debe ingresar 0 para estado inactivo y 1 para estado activo."
    )


    def get(self):
        return {'cursos': list(map(lambda x: x.obtener_datos(), CursoModel.query.all()))}


    def post(self):
        data = Cursos.parser.parse_args()
        if CursoModel.buscar_existencia(data['nombre']):
            return {'message': "Ya existe un curso llamado '{}'. Póngase creativo!".format(data['nombre'])}, 400

        if ProfesorModel.buscar_por_id(data['id_profesor']):
            curso = CursoModel(data['nombre'],data['nivel'],data['id_profesor'])
            curso.activo = data['activo'] if data['activo'] else None
            curso.activo = data['activo'] == 0 if data['activo'] else None
            try:
                curso.guardar()
            except:
                return {"message": "No se pudo resolver su petición."}, 500
            return curso.obtener_datos(), 201

        else :
            return {'message': "El identificador del profesor ingresado no es válido"}, 400



class AlumnosCurso(Resource):


    def get(self, _id):
        curso = CursoModel.buscar_por_id(_id)
        if curso:
            return curso.obtener_alumnos()
        return {'mensaje': 'No se encontró el recurso solicitado'}, 404
