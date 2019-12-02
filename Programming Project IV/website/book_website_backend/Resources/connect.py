#!/usr/bin/python3
import cx_Oracle, pandas as pd, sys, csv, codecs, os

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

    def get_query_data(self, command):
        self.cursor.execute(command)
        rows = self.cursor.fetchall()
        return rows

    def run_command(self, command):
        self.establish_connection()
        self.execute_command(command)
        self.commit_changes()
        self.close_connection()

if __name__ == "__main__":
    conn =Connect(
                    'ora-scsp.srv.mst.edu',
                    1521,
                    os.environ['DBEAVER_USERNAME'],
                    os.environ['DBEAVER_PASSWORD'],
                    'scsp.mst.edu'
                )

    conn.establish_connection()
    data = conn.get_query_data('SELECT * FROM CAO346.AUTHORS')
    for row in data:
        print(row[0])
    conn.close_connection()
