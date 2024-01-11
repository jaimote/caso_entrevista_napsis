#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,click

#sys.path.insert(0, os.path.join( os.path.dirname(os.path.abspath(__file__)) ,'modelos'))
from flask import Flask, request
from flask_restful import Api
from aplicacion.config import app_config
from aplicacion.db import db
from aplicacion.modelos import *
from sqlalchemy import text

from aplicacion.recursos.usuario import Usuario, Usuarios
from aplicacion.recursos.alumno import Alumno, Alumnos, CursosAlumno
from aplicacion.recursos.profesor import Profesor, Profesores, CursosProfesor
from aplicacion.recursos.curso import Curso, Cursos, AlumnosCurso

# IMPORTACIÓN DE RECURSOS

app = Flask(__name__)

#Se establece enviroment como argumento
#enviroment = sys.argv[1]
enviroment ="development"

#Se setean variables de configuracion segun ambiente(env)
app.config.from_object(app_config[enviroment])
db.init_app(app)
api = Api(app)

# SE DEFINEN LOS ENDPOINTS Y LA CLASE QUE SE ENCARGARÁ DE PROCESAR CADA SOLICITUD
api.add_resource(Usuario, '/usuario/<int:_id>')
api.add_resource(Usuarios, '/usuarios')
api.add_resource(Alumno, '/alumno/<int:_id>')
api.add_resource(Alumnos, '/alumnos')
api.add_resource(CursosAlumno, '/alumno/<int:_id>/cursos')
api.add_resource(Profesor, '/profesor/<int:_id>')
api.add_resource(CursosProfesor, '/profesor/<int:_id>/cursos')
api.add_resource(Profesores, '/profesores')
api.add_resource(Curso, '/curso/<int:_id>')
api.add_resource(Cursos, '/cursos')
api.add_resource(AlumnosCurso, '/curso/<int:_id>/alumnos')

app.run(host='0.0.0.0',port=5000)