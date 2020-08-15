# -*- coding: utf-8 -*-
import json
import io
import base64
from PIL import Image
from werkzeug.security import generate_password_hash, check_password_hash
from db.data_controller import DataController
from config.settings import getConfig
from utils.format_objects import getObjById, buildMsgEmail, removeEmptyData


admin_control = None
MAIL_MESSAGES = getConfig().get('mail_messages')

with open(MAIL_MESSAGES) as config_file:
    config = json.load(config_file)
    admin_messages = config.get('admin')
    admin_msg_sign = admin_messages['sign']
    admin_msg_login = admin_messages['login']
    admin_msg_update = admin_messages['update']

class AdminService:
    def __init__(self, email_sender):
        self.email_sender = email_sender
        self.admin_control = admin_control
        if not self.admin_control:
            admin_props = {
                'table_name': 'tbl_administradores_transf',
                'prefix': 'admin_',
                'file_field': ['imagen']
            }
            self.admin_control = DataController(admin_props)


    def addAdmin(self, data):
        subject = 'Registro homologaciones CUN'
        admin_msg = None
        data['password'] = generate_password_hash(data.get('id'), method='pbkdf2:sha256', salt_length=10)
        admin_name = (data.get('nombres'), data.get('apellidos'))
        if not self.admin_control.findById(data.get('id')):
            f = {
                'and': [
                    {
                        'variable': 'email',
                        'comparisson': '=',
                        'value': "'{}'".format(data.get('email'))
                    }
                ]
            }
            if not self.admin_control.findByFilter(f):
                if self.admin_control.add(data):
                    admin_msg = buildMsgEmail(admin_msg_sign, admin_name)
                    info = 201, 'Server: Admin Added'
                else:
                    aux_msg = "Hubo un fallo en el registro"
                    admin_msg = buildMsgEmail(admin_msg_sign, admin_name, aux_msg)
                    info = 304, 'Server: Not Modified'
            else:
                info = 400, 'Server: Bad request, duplicate email'
        else:
            info = 409, 'Server: Conflict, Admin exists'

        # Send Message
        if admin_msg:
            print (self.email_sender.sendMessage(subject, admin_msg, [data.get('email')]))
        return info

    def getAdminById(self, id):
        user =  getObjById(id, self.admin_control)
        if not user:
            return 404, "Admin not found"
        del user['password']
            # if user.get('imagen'):
            #     img = Image.open(user.get('imagen'), mode='r')
            #     imgByteArr = io.BytesIO()
            #     imgByteArr = imgByteArr.getvalue()
            #     imgByteArr = base64.encodebytes(imgByteArr).decode('ascii')
            #     user['imagen'] = imgByteArr
        return 200, user


    def loginAdmin(self, data):
        subject = 'Ingreso a Homologaciones CUN'
        admin_msg = None
        user = None
        id = data.get('id')
        if id:
            user = self.admin_control.findById(id)
        else:
            ftr = {
                'and': [
                    {
                        'variable': 'email',
                        'comparisson': '=',
                        'value': "'{}'".format(data.get('email'))
                    }
                ]
            }
            user = self.admin_control.findByFilter(ftr)
        if user:
            fuser = getObjById(user[0], self.admin_control)
            if check_password_hash(fuser.get('password'), data.get('password')):
                admin_name = (fuser.get('nombres'), fuser.get('apellidos'))
                admin_msg = buildMsgEmail(admin_msg_login, admin_name)
                self.email_sender.sendMessage(subject, admin_msg, [fuser.get('email')])
                return 200, id
            return 401, 'Server: Admin Unauthorized'
        return 404, 'Server: Admin not found'

    def updateData(self, id, data):
        admin_msg = None
        subject = 'Actualizacion de Cuenta'
        data = removeEmptyData(data)
        new_pwd = data.get('password')
        if new_pwd:
            if new_pwd == data.get('conf_password'):
                del data['conf_password']
                del data['password']
                data['password'] = generate_password_hash(new_pwd, method='pbkdf2:sha256', salt_length=10)
            else:
                return 400, 'Bad Request, different passwords'
        admin = getObjById(id, self.admin_control)
        admin_name = (admin.get('nombres'), admin.get('apellidos'))
        if self.admin_control.update(data, id):
            admin_msg = buildMsgEmail(admin_msg_update, admin_name)
            info =  200, 'Admin Modified'
        else:
            fail_msg = "Ha habido un fallo en el proceso de actualizacion"
            admin_msg = buildMsgEmail(admin_msg_update, admin_name, fail_msg)
            info = 304, 'Not Modified'
        self.email_sender.sendMessage(subject, admin_msg, [admin.get('email')])
        return info
