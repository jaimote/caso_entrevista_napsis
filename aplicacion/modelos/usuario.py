#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aplicacion.db import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from aplicacion.helpers.utilidades import Utilidades

class UsuarioModel(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    salt = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    activo = db.Column(db.SMALLINT, nullable=True, default=1)

    def __init__(self, username, password):
        # self._id = id
        self.username = username
        self.salt = None
        self.password = password
        self.activo = 1

    def obtener_datos(self):
        return {'id': self.id, 'username': self.username, 'activo':  self.activo}

    @classmethod
    def buscar_por_id(cls, _id):
        # Usamos _id (con el guion bajo) porque id solito es una palabra reservada de Python <0>
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def buscar_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
