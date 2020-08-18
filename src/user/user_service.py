# -*- coding: utf-8 -*-
import json
from PIL import Image
from werkzeug.security import generate_password_hash, check_password_hash
from src.db.data_controller import DataController
from src.transference.assignement_controller import AssignementController
from src.utils.format_objects import getObjById, buildMsgEmail, removeEmptyData
from src.config.settings import getConfig
user_control = None

MAIL_MESSAGES = getConfig().get('mail_messages')

with open(MAIL_MESSAGES) as config_file:
    config = json.load(config_file)
    user_messages = config.get('user')
    user_msg_sign= user_messages['sign']
    user_msg_login = user_messages['login']
    user_msg_update = user_messages['update']

    admin_messages = config.get('admin')
    admin_msg_sign = admin_messages['sign_user']

    managers_data = config.get('managers')
    serv_std = managers_data.get('servicio_estudiante')
    cargo = serv_std.get('cargo')
    cod_secc = serv_std.get('cod_secc')
    cod_sede = serv_std.get('cod_sede')


class UserService:
    def __init__(self, email_sender):
        self.email_sender = email_sender
        self.user_control = user_control
        self.assig_control = AssignementController()
        if not self.user_control:
            user_props = {
                'table_name': 'tbl_usuarios_transf',
                'prefix': 'u_',
                'file_field': ['imagen']
            }
            self.user_control = DataController(user_props)


    def addUser(self, data):
        subject = 'Registro homologaciones CUN'
        user_msg = admin_msg = None
        data['password'] = generate_password_hash(data.get('id'),
            method='pbkdf2:sha256',
            salt_length=10)
        f = {
            'and': [
                {
                    'variable': 'email',
                    'comparisson': '=',
                    'value': "'{}'".format(data.get('email'))
                }
            ]
        }
        user_mail = self.user_control.findByFilter(f)
        admin = self.assig_control.defineManager(cargo, cod_secc, cod_sede)
        admin_name = (admin.get('nombres'), admin.get('apellidos'))
        if not getObjById(data.get('id'), self.user_control):
            if not user_mail:
                user_name = (data.get('nombres'), data.get('apellidos'))
                if self.user_control.add(data):
                    user_msg = buildMsgEmail(user_msg_sign, user_name)
                    del data['password']
                    admin_msg = buildMsgEmail(admin_msg_sign, admin_name, data)
                    info = 201, 'Server: User Added'
                else:
                    aux_message = 'Fallo en registro de usuario'
                    user_msg = buildMsgEmail(user_msg_sign, user_name, aux_message)
                    admin_msg = buildMsgEmail(admin_msg_sign, admin_name, aux_message)
                    info = 304, 'Server: Not Modified'
            else:
                info = 400, 'Server: Bad request, duplicate email'
        else:
            info = 409, 'Server: Conflict, User exists'

        # Send Email
        if user_msg:
            self.email_sender.sendMessage(subject, user_msg, [data.get('email')])
        if admin_msg:
            self.email_sender.sendMessage(subject, admin_msg, [admin.get('email')])
        return info

    def loginUser(self, data):
        subject = 'Ingreso a Homologaciones CUN'
        user_msg = None
        user = None
        id = data.get('id')
        if id:
            user = self.user_control.findById(id)
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
            user = self.user_control.findByFilter(ftr)[-1]
        if user:
            fuser = getObjById(user[0], self.user_control)
            if check_password_hash(fuser.get('password'), data.get('password')):
                user_name = (fuser.get('nombres'), fuser.get('apellidos'))
                user_msg = buildMsgEmail(user_msg_login, user_name)
                self.email_sender.sendMessage(subject, user_msg, [fuser.get('email')])
                return 200, id
            return 401, 'User Unauthorized'
        return 404, 'User not found'

    def getUserById(self, id):
        user =  getObjById(id, self.user_control)
        if not user:
            return 404, "User not found"
        del user['password']
            # if user.get('imagen'):
            #     img = Image.open(user.get('imagen'), mode='r')
            #     imgByteArr = io.BytesIO()
            #     imgByteArr = imgByteArr.getvalue()
            #     imgByteArr = base64.encodebytes(imgByteArr).decode('ascii')
            #     user['imagen'] = imgByteArr
        return 200, user

    def updateData(self, id, data):
        user_msg = None
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
        user = getObjById(id, self.user_control)
        user_name = (user.get('nombres'), user.get('apellidos'))
        if self.user_control.update(data, id):
            user_msg = buildMsgEmail(user_msg_update, user_name)
            info =  200, 'Admin Modified'
        else:
            fail_msg = "Ha habido un fallo en el proceso de actualizacion"
            admin_msg = buildMsgEmail(user_msg_update, user_name, fail_msg)
            info = 304, 'Not Modified'
        self.email_sender.sendMessage(subject, user_msg, [user.get('email')])
        return info
