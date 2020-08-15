# -*- coding: utf-8 -*-
import datetime
from db.data_controller import DataController
from utils.format_objects import formatObjToDict, getObjById

manager_control = None
admin_control = None

class AssignementController:
    def __init__(self):
        self.manager_control = manager_control
        self.admin_control = admin_control
        if not self.manager_control:
            manager_props = {
                'table_name': 'tbl_encargados_transf',
                'prefix': 'e_',
                'file_field': []
            }
            self.manager_control = DataController(manager_props)
        if not self.admin_control:
            admin_props = {
                'table_name': 'tbl_administradores_transf',
                'prefix': 'admin_',
                'file_field': []
            }
            self.admin_control = DataController(admin_props)


    def defineManager(self, cargo, cod_secc, cod_sede, transf=None):
        print('Server: Defining manager')
        f = {
            'and': [
                {
                    'variable': 'disponibilidad',
                    'comparisson': '=',
                    'value': 1
                },
                {
                    'variable': 'cargo',
                    'comparisson': '=',
                    'value': "'{}'".format(cargo)
                },
                {
                    'variable': 'cod_secc',
                    'comparisson': '=',
                    'value': "'{}'".format(cod_secc)
                },
                {
                    'variable': 'cod_sede',
                    'comparisson': '=',
                    'value': "'{}'".format(cod_sede)
                }
            ]
        }
        user_id = self.admin_control.findByFilter(f)
        if not user_id:
            data_upt = {
                        "disponibilidad": 1
                    }
            filter_upt = f
            filter_upt['and'][0] = {
                'variable': 'disponibilidad',
                'comparisson': '=',
                'value': 0
            }
            data_updated = True if self.admin_control.updateAllData(data_upt, filter_upt) else False
            print('Server: User distribution prepared' if data_updated else 'Server: Error in user distribution')
            return self.defineManager(cargo, cod_secc, cod_sede, transf)
        data =  getObjById(user_id[0][0], self.admin_control)
        data_upt = {
            "disponibilidad": 0
        }
        asigned = self.modifyManagers(data.get('id'), transf)
        print('Server: Admin Asigned'if asigned else 'Error: Error in admin Assination')
        data_updated = True if self.admin_control.update(data_upt, data.get('id')) else False
        print('Server: User distribution prepared' if data_updated else 'Server: Error in user distribution')
        return data

    def modifyManagers(self, assigned, transf, dispatcher='default'):
        assignment = {
            'transferencia_asignada': transf,
            'admin_encargado': assigned,
            'fecha_asignacion': datetime.datetime.now(),
            'admin_asignador': dispatcher
        }
        return self.manager_control.add(assignment)

    def getTransferencesAssigned(self, id_admin):
        filt = {
            'and':[
                {
                    'variable': 'admin_encargado',
                    'comparisson': '=',
                    'value': id_admin
                }
            ]
        }
        params = self.manager_control.paramsData()
        data = []
        for transf in self.manager_control.findByFilter(filt):
            data.append(formatObjToDict(params, transf))
        return data

    def getManagersTransf(self, id_transf):
        filt = {
            'and':[
                {
                    'variable': 'transferencia_asignada',
                    'comparisson': '=',
                    'value': "'{}'".format(id_transf)
                }
            ]
        }
        params = self.manager_control.paramsData()
        data = []
        all_transf = self.manager_control.findByFilter(filt)
        if all_transf:
            for transf in all_transf:
                data.append(formatObjToDict(params, transf))
            return data
        return False
