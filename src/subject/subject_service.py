# -*- coding: utf-8 -*-
from db.data_controller import DataController
from utils.format_objects import getObjById, formatObjToDict
subject_control = None

class SubjectService():
    def __init__(self):
        self.subject_control = subject_control
        if not self.subject_control:
            subject_props = {
                'table_name': 'tbl_materias_vistas',
                'prefix': 'm_',
                'file_field': []
            }
            self.subject_control = DataController(subject_props)

    def addSubject(self, data):
        if self.subject_control.add(data):
            return 200, 'Subject Added'
        return 500, 'Internal Server Error'

    def getAllSubjects(self, transf_id):
        filt = {
            'and': [
            {
                'variable': 'transferencia_id',
                'comparisson': '=',
                'value': "'{}'".format(transf_id)
            }
            ]
        }
        keys = self.subject_control.paramsData()
        all_data = self.subject_control.findByFilter(filt)
        subjects = []
        if keys and all_data:
            for data in all_data:
                subjects.append(formatObjToDict(keys, data))
        return 200, subjects

    def getSubject(self, id):
        data = getObjById(id, self.subject_control)
        if data:
            return 200, data
        return 404, 'Subject not found'
