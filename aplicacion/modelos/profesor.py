#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aplicacion.db import db
from sqlalchemy.sql import expression

class ProfesorModel(db.Model):
    __tablename__ = 'profesor'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombress = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, server_default=expression.true())


    def __init__(self, nombres, apellidos):
        self._id = None
        self.nombres = nombres
        self.apellidos = apellidos
        self.activo = True



    # Se puede ver que usamos funciones que llevan el decorador @classmethod
    # La diferencia está en que las que NO llevan el decorador se inicializan con
    # una instancia de la clase, por ende, requiere una instancia de la clase.
    # Con el decorador classmethod inicializamos implícitamente con la clase misma.
    # En este caso particular, los usamos para crear una instancia de la clase
    # en base a una consulta a la base de datos.
    # También existe el decorador @staticmethod, con lo que la función no recibe
    # implicitamente ni la clase ni una instancia de la clase. Por esto, puede ser
    # utilizada desde otra funcion de la clase o desde una instancia de esta.

    def obtener_datos(self):
        return {'id': self.id, 'nombres': self.nombres, 'apellidos': self.apellidos, 'activo': self.activo}

    @classmethod
    def buscar_por_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def buscar_existencia(cls, nombres, apellidos):
        return cls.query.filter_by(nombres=nombres).filter_by(apellidos=apellidos).first()

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
