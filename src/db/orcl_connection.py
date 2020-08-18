# -*- coding: utf-8 -*-
import cx_Oracle
from src.config.settings import getConfig

connection = None
db_config = getConfig().get('db_config')

class Connection:
    def __init__(self):
        self.conn = None
        self.cursor = None
        if not self.conn:
            try:
                dsn = cx_Oracle.makedsn(db_config.get('host'), int(db_config.get('port')),db_config.get('service'))
                self.conn = cx_Oracle.connect(db_config.get('user'), db_config.get('password'), dsn)
                self.cursor = self.conn.cursor()
                print('Database: Database Connected')
            except cx_Oracle.Error as error:
                print('ERROR DB:', error)

    def getConnectionData(self):
        return self.conn, self.cursor

    def disconnect(self):
        self.conn.close()
