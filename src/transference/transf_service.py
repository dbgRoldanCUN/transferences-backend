# -*- coding: utf-8 -*-
import datetime
import json
from src.db.data_controller import DataController
from src.transference.assignement_controller import AssignementController
from src.config.settings import getConfig
from src.utils.format_objects import getObjById, buildMsgEmail, formatObjToDict

transf_control = None
user_control = None

MAIL_MESSAGES = getConfig().get('mail_messages')

with open(MAIL_MESSAGES) as config_file:
    config = json.load(config_file)
    admin_messages = config.get('admin')
    admin_msg_transf = admin_messages.get('transf_created')
    admin_msg_upt_transf = admin_messages.get('transf_update')

    user_messages = config.get('user')
    user_msg_transf = user_messages.get('transf_created')
    user_msg_upt_transf = user_messages.get('transf_update')

    managers_data = config.get('managers')
    registro_control = managers_data.get('registro_control')
    rc_cargo = registro_control.get('cargo')
    rc_cod_secc = registro_control.get('cod_secc')
    rc_cod_sede = registro_control.get('cod_sede')

    analista_registro = managers_data.get("analista_registro")
    anr_cargo = analista_registro.get('cargo')
    anr_cod_secc = analista_registro.get('cod_secc')
    anr_cod_sede = analista_registro.get('cod_sede')

    auxiliar_registro = managers_data.get("auxiliar_registro")
    axr_cargo = auxiliar_registro.get('cargo')
    axr_cod_secc = auxiliar_registro.get('cod_secc')
    axr_cod_sede = auxiliar_registro.get('cod_sede')


class TransferenceService():
    def __init__(self, email_sender):
        self.transf_control = transf_control
        self.user_control = user_control
        self.email_sender = email_sender
        self.assig_control = AssignementController()
        if not self.transf_control:
            transf_props = {
                'table_name': 'tbl_transferencias_transf',
                'prefix': 't_',
                'file_field': ['notas', 'transf_carta']
            }
            self.transf_control = DataController(transf_props)
        if not self.user_control:
            user_props = {
                'table_name': 'tbl_usuarios_transf',
                'prefix': 'u_',
                'file_field': ['imagen']
            }
            self.user_control = DataController(user_props)


    def showAdminTransf(self, id_admin):
        data = self.assig_control.getTransferencesAssigned(id_admin)
        return 200, data

    def showTransf(self, id):
        data = getObjById(id, self.transf_control)
        if not data:
            return 404, 'Transference data not found'
        return 200, data

    def addTransference(self, data, user_id):
        subject = 'Registro de Transferencia'
        user_msg = None
        user = getObjById(user_id, self.user_control)
        user_name = (user.get('nombres'), user.get('apellidos'))
        if self.transf_control.add(data):
            admin = self.assig_control.defineManager(rc_cargo, rc_cod_secc, rc_cod_sede, data.get('id'))
            admin_name = (admin.get('nombres'), admin.get('apellidos'))
            admin_msg = buildMsgEmail(admin_msg_transf, admin_name, {'CC': user.get('id')})

            self.email_sender.sendMessage(subject, admin_msg,
             [admin.get('email')], [data.get('transf_carta')])

            user_msg = buildMsgEmail(user_msg_transf, user_name)
            info = 200, 'Transference Added'
        else:
            fail_msg = "Ha habido un fallo en su proceso de crecion de transferencia"

            user_msg = buildMsgEmail(user_msg_transf, admin_name, fail_msg)
            info = 304, 'Not Modified'
        self.email_sender.sendMessage(subject, user_msg, [user.get('email')])
        return info

    def showUserTransf(self, id):
        filter = {
            'and': [
            {
                'variable': 'usuario_id',
                'comparisson': '=',
                'value': "'{}'".format(id)
            }
            ]
        }
        keys = self.transf_control.paramsData()
        all_data = self.transf_control.findByFilter(filter)
        transferences = []
        for data in all_data:
            transferences.append(formatObjToDict(keys, data))
        return 200, transferences

    def updateTransference(self, data, id_transf):
        subject = 'Actualizacion de Transferencia'
        user_msg = admin_msg_aux = admin_msg_anr = None

        current_trasnf = getObjById(id_transf, self.transf_control)
        user = getObjById(current_trasnf.get('usuario_id'), self.user_control)
        user_name = (user.get('nombres'),user.get('apellidos'))
        if self.transf_control.update(data, id_transf):
            if not 'borrado' in list(data.keys()):
                admin_aux_reg = self.assig_control.defineManager(axr_cargo, axr_cod_secc, axr_cod_sede, id_transf)
                admin_anr_reg = self.assig_control.defineManager(anr_cargo, anr_cod_secc, anr_cod_sede, id_transf)

                admin_aux_name = (admin_aux_reg.get('nombres'), admin_aux_reg.get('apellidos'))
                admin_anr_name = (admin_anr_reg.get('nombres'), admin_anr_reg.get('apellidos'))
                user_data = {'C.c.': user.get('id')}

                admin_msg_aux = buildMsgEmail(admin_msg_upt_transf, admin_aux_name, user_data)
                admin_msg_anr = buildMsgEmail(admin_msg_upt_transf, admin_anr_name, user_data)

                self.email_sender.sendMessage(subject, admin_msg_anr, [admin_anr_reg.get('email')])
                self.email_sender.sendMessage(subject, admin_msg_aux, [admin_aux_reg.get('email')])
            user_msg = buildMsgEmail(user_msg_upt_transf, user_name)
            info = 200, 'Tranference Modified'
        else:
            fail_msg = "Ha habido un fallo en el proceso de actualizacion"
            user_msg = buildMsgEmail(user_msg_upt_transf, user_name, fail_msg)
            info = 304, 'Not Modified'
        self.email_sender.sendMessage(subject, user_msg, [user.get('email')])
        return info

    def deleteTrasnference(self, id):
        user_msg = None
        data = {
            'archivo_aprobado': 'ninguno',
            'estado': 'Eliminado',
            'borrado': datetime.datetime.now()
        }
        return self.updateTransference(data, id)

    def getManagers(self, id):
        data = self.assig_control.getManagersTransf(id)
        if data:
            return 200, data
        return 404, 'Managers not found'

    def assignManager(self, id, assign):
        assigned = assign.get('asignado')
        if not assigned or assigned == '':
            assigned = 'default'
        if assigned == 'default':
            admin_props = {
                'table_name': 'tbl_administradores_transf',
                'prefix': 'admin_',
                'file_field': ['imagen']
            }
            admin_control = DataController(admin_props)
            current_admin = getObjById(assign.get('asignador'), admin_control)
            asign = self.assig_control.defineManager(current_admin.get('cargo'), current_admin.get('cod_secc'), current_admin.get('cod_sede'), id)
        else:
            asign = self.assig_control.modifyManagers(assigned, id,
            assign.get('asignador'))
        if asign:
            return 200, 'New Managaer assigned'
        return 500, 'Fail in new manager assignement'
