#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from aplicacion.modelos.alumno import AlumnoModel

class Alumno(Resource):

    def get(self, _id):
        """
            @apiGroup Alumno
            @apiName Buscar alumno
            @api {get} /alumno/:id
            @apiVersion 1.0.0
            @apiDescription Busca un alumno por su id
            @apiExample {json} Example-Response:
                {
                    "id": 1,
                    "nombres": "Florencia",
                    "apellidos": "Padilla",
                    "fecha_inscripcion": "25-03-2018",
                    "activo": true
                }
        """
        alumno = AlumnoModel.buscar_por_id(_id)
        if alumno:
            return alumno.obtener_datos()
        return {'mensaje': 'No se encontró el recurso solicitado'}, 404

    def delete(self, _id):
        alumno = AlumnoModel.buscar_por_id(_id)
        if alumno:
            try:
                alumno.eliminar()
                return {'message': 'Alumno eliminado con éxito'}
            except Exception as e:
                return {'message': 'No se pudo realizar la eliminación'}, 500
        else :
            return {'mensaje': 'No se encontró el recurso solicitado'}, 404



class Alumnos(Resource):

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
        help="Debe ingresar un nombre para el alumno"
    )
    parser.add_argument('apellidos',
        type=str,
        required=True,
        help="Debe ingresar un apellido para el alumno."
    )
    parser.add_argument('activo',
        type=int,
        required=False,
        choices=(0, 1),
        help="Debe ingresar 0 para estado inactivo y 1 para estado activo."
    )


    def get(self):
        return {'alumnos': list(map(lambda x: x.obtener_datos(), AlumnoModel.query.all()))}


    def post(self):
        data = Alumnos.parser.parse_args()
        if AlumnoModel.buscar_existencia(data['nombres'],data['apellidos']):
            return {'message': "Ya existe un alumno llamado '{} {}'. Uno es suficiente!".format(data['nombres'], data['apellidos'])}, 400
        alumno = AlumnoModel(data['nombres'],data['apellidos'])
        alumno.activo = data['activo'] if data['activo'] else None
        try:
            alumno.guardar()
        except:
            return {"message": "No se pudo resolver su petición."}, 500
        return alumno.obtener_datos(), 201

    # La acción PUT ingresa un recurso en caso de que no exista. Si existe actualiza todos los valores
    def put(self):
        data = Alumnos.parser.parse_args()
        if AlumnoModel.buscar_existencia(data['nombres'],data['apellidos']):
            alumno = AlumnoModel.buscar_existencia(data['nombres'],data['apellidos'])
        else :
            alumno = AlumnoModel(data['nombres'],data['apellidos'])

        alumno.activo = data['activo'] if data['activo'] else None

        try:
            alumno.guardar()
        except:
            return {"message": "No se pudo resolver su petición."}, 500
        return alumno.obtener_datos(), 201


class CursosAlumno(Resource):

    def get(self, _id):
        alumno = AlumnoModel.buscar_por_id(_id)
        if alumno:
            cursos = alumno.cursos
            listaCursos = {}
            for curso in cursos:
                dataProfesor = {'id': curso.id_profesor, 'nombres':curso.profesor.nombres,
                    'apellidos':curso.profesor.apellidos}
                listaCursos[curso.id] = {"nombre":curso.nombre,"nivel":curso.nivel,"id_profesor":curso.id_profesor,"profesor":dataProfesor}
            dataAlumno = alumno.obtener_datos()
            dataAlumno['cursos'] = listaCursos
            return dataAlumno
        return {'mensaje': 'No se encontró el recurso solicitado'}, 404
