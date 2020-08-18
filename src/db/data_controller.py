# -*- coding: utf-8 -*-
import datetime
import cx_Oracle
from src.db.orcl_connection import Connection
from src.utils.filter_generators import generateSQLFilter


class DataController:
    def __init__(self, props):
        connection = Connection()
        self.conn, self.cursor = connection.getConnectionData()
        self.table_name = props.get('table_name')
        self.prefix = props.get('prefix')
        self.file_field = props.get('file_field')

    def add(self, data):
        params = self.paramsData()
        if 'creado' in params:
            data['creado'] = datetime.datetime.now()

        query = 'INSERT INTO {}('.format(self.table_name)
        attrbs_data = list(data.keys())
        query_data = ''

        data_arr = []
        for attrb in attrbs_data:
            comma = '' if data.get(attrb) is data.get(attrbs_data[0]) else ', '
            query += '{}{}{}'.format(comma, self.prefix, attrb)
            data_arr.append(data.get(attrb))
            query_data += '{}:{}{}'.format(comma, self.prefix, attrb)
        query += ') VALUES({})'.format(query_data)

        try:
            self.cursor.execute(query, data_arr)
            self.conn.commit()
            print('DB: New Data Added')
            return True
        except cx_Oracle.Error as error:
            print('ERROR DB:', error)
            return False

    def findById(self, id):
        query = "SELECT * FROM {} WHERE {}id = '{}'".format(self.table_name, self.prefix, id)

        try:
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            return row
        except cx_Oracle.Error as error:
            print('ERROR DB**', error)
            return False

    def findByFilter(self, filter):
        query = "SELECT * FROM {} WHERE ".format(self.table_name)
        query += generateSQLFilter(filter, self.prefix, ['and'])

        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except cx_Oracle.Error as error:
            print('ERROR DB', error)
            return False

    def update(self, data, data_id):
        if 'actualizado' in self.paramsData():
             data['actualizado'] = datetime.datetime.now()
        attrbs_data = list(data.keys())
        query_stat = ''
        data_arr = []
        for attrb in attrbs_data:
            comma = '' if data.get(attrb) is data.get(attrbs_data[0]) else ', '
            query_stat+= '{}{}{} = :{}{}'.format(comma, self.prefix, attrb, self.prefix, attrb)
            data_arr.append(data.get(attrb))
        query = 'UPDATE {} SET {} WHERE {}'.format(self.table_name,
            query_stat,
            "{}id = :{}id ".format(self.prefix, self.prefix)
            )
        data_arr.append(data_id)
        data_arr = tuple(data_arr)
        try:
            self.cursor.execute(query, tuple(data_arr))
            self.conn.commit()
            print('DB: Data updated')
            return True
        except cx_Oracle.Error as error:
            print('ERROR DB:', error)
            return False

    def updateAllData(self, data, filter):
        attrbs_data = list(data.keys())
        data_arr = []
        query_stat = ''
        for attrb in attrbs_data:
            comma = '' if data.get(attrb) is data.get(attrbs_data[0]) else ', '
            query_stat+= '{}{}{}= :{}{}'.format(comma, self.prefix, attrb, self.prefix, attrb)
            data_arr.append(data.get(attrb))
        query = 'UPDATE {} SET {} WHERE {}'.format(self.table_name,
            query_stat,generateSQLFilter(filter, self.prefix, ['and']))

        try:
            self.cursor.execute(query, data_arr)
            self.conn.commit()
            print('DB: Data updated')
            return True
        except cx_Oracle.Error as error:
            print('ERROR DB:', error)
            return False

    def paramsData(self):
        query = """SELECT column_name FROM USER_TAB_COLUMNS WHERE table_name = '{}'""".format(self.table_name)
        try:
            r = self.cursor.execute("SELECT * FROM {}".format(self.table_name))
            col_def_names = [row[0] for row in self.cursor.description]
            col_names = []
            for col in col_def_names:
                col_names.append(col[len(self.prefix):].lower())
            return col_names
        except cx_Oracle.Error as error:
            print('ERROR DB ', error)
            return False

    def addFile(self, field_file, path_file, id):
        file = open(path_file, 'rb')
        content = file.read()
        file.close()
        blobvar = self.cursor.var(cx_Oracle.BLOB)
        blobvar.setvalue(0,content)
        self.cursor.setinputsizes (blobData = cx_Oracle.BLOB)
        query = "UPDATE {} SET {}=:blobData WHERE u_id='{}'".format(self.table_name, field_file, id)
        try:
            self.cursor.execute(query, {'blobData':blobvar})
            return True
        except cx_Oracle.Error as error:
            print('ERROR DB:', error)
            return False
