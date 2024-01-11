#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_script import Manager
from aplicacion.app import app,db
from getpass import getpass


manager = Manager(app)
#app.config['DEBUG'] = True # Ensure debugger will load.

if __name__ == '__main__':
    manager.run()
