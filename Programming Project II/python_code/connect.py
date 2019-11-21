#!/usr/bin/python3
import cx_Oracle, pandas as pd, sys, csv, codecs

class Connect():
    def __init__(self, host, port, user, psw, service):
        self.CONN_INFO = {
                'host': host ,
                'port':  port,
                'user': user ,
                'psw': psw,
                'service': service
        }
        self.CONN_STR = '{user}/{psw}@{host}:{port}/{service}'.format(**self.CONN_INFO)
        self.cursor = ''
        self.connection = ''

    def establish_connection(self):
        self.connection = cx_Oracle.connect(self.CONN_STR)
        self.cursor = self.connection.cursor()

    def commit_changes(self):
        self.connection.commit()
    
    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def execute_command(self, command):
        self.cursor.execute(command)

    def run_command(self, command):
        self.establish_connection()
        self.execute_command(command)
        self.commit_changes()
        self.close_connection()

if __name__ == "__main__":
    connection =Connect(
                    'ora-scsp.srv.mst.edu',
                    1521,
                    'username',
                    'password',
                    'scsp.mst.edu'
                )
    connection.establish_connection()
    connection.close_connection()
