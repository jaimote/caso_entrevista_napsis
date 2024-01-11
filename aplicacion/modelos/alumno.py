#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aplicacion.db import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from aplicacion.helpers.utilidades import Utilidades
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.sql import expression



class AlumnoModel(db.Model):
    __tablename__ = 'alumno'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    fecha_inscripcion = db.Column(db.TIMESTAMP, nullable=False,default=datetime.utcnow)
    activo = db.Column(db.Boolean, nullable=False, server_default=expression.true())


    def __init__(self, nombres, apellidos, fecha_inscripcion=None):
        # self._id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.fecha_inscripcion = fecha_inscripcion
        self.activo = True


    def obtener_datos(self):
        fechaInscripcion = Utilidades.formatoFecha(self.fecha_inscripcion)
        return {'id': self.id, 'nombres': self.nombres, 'apellidos': self.apellidos, 'fecha_inscripcion': fechaInscripcion, 'activo':  self.activo}



    # Se puede ver que usamos funciones que llevan el decorador @classmethod
    # La diferencia está en que las que NO llevan el decorador se inicializan con
    # una instancia de la clase, por ende, requiere una instancia de la clase.
    # Con el decorador classmethod inicializamos implícitamente con la clase misma.
    # En este caso particular, los usamos para crear una instancia de la clase
    # en base a una consulta a la base de datos.
    # También existe el decorador @staticmethod, con lo que la función no recibe
    # implicitamente ni la clase ni una instancia de la clase. Por esto, puede ser
    # utilizada desde otra funcion de la clase o desde una instancia de esta.

    @classmethod
    def buscar_por_id(cls, _id):
        # Usamos _id (con el guion bajo) porque id solito es una palabra reservada de Python <0>
        return cls.query.filter_by(id=_id).first()

    # Busca si existe un alumno con igual nombre y apellido.
    # No permitiremos el ingreso de coinsidencias de nombre-apellido para ejemplificar el uso de multiples filtros.
    @classmethod
    def buscar_existencia(cls, nombres, apellidos):
        return cls.query.filter_by(nombres=nombres).filter_by(apellidos=apellidos).first()

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
