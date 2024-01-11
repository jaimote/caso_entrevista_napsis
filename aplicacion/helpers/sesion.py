#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from aplicacion.db import db
from sqlalchemy import text
import random
import hashlib
from datetime import datetime
from aplicacion.redis import redis
from aplicacion.helpers.utilidades import Utilidades


class Sesion():

    @staticmethod
    def generar_tokenid(time, password, username, id_usuario):
        # return None
        try:
            fecha_actual = datetime.now()
            base = username+password+str(fecha_actual.minute)+str(fecha_actual.second)
            token_id = hashlib.md5(base.encode()).hexdigest()
            data = {
                "username":username,
                "id_persona":id_persona,
                "id_usuario":id_usuario
            }
            redis.setex(token_id, time, json.dumps(data))
            data = redis.get(token_id)
            return token_id
        except Exception as e:
            # return Utilidades.exceptionInfo(e)
            return None


    @staticmethod
    def eliminar_tokenid(token_id):
        try:
            redis.delete(token_id)
            return True
        except Exception as e:
            return None
    
    @staticmethod
    def validar_token(token_id):
        existe = redis.exists(token_id)
        return existe
    
    @staticmethod
    def generate_hash(password):
        hash_final = hashlib.sha1(hashlib.md5(hashlib.md5(hashlib.md5(password.encode()).hexdigest().encode()).hexdigest().encode()).hexdigest().encode()).hexdigest()
        return hash_final
