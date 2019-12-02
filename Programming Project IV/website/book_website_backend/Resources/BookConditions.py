#!/usr/bin/python3
from flask import Flask 
from flask_restful import Api, Resource, reqparse, fields, request
from flask_cors import CORS
from connect import Connect
import os, pandas, debug

app = Flask(__name__)
api = Api(app)
CORS(app)

jacket_conditions_fields = {
    'jacket_conditions': fields.String
}

class BookConditions(Resource):
    def __init__(self):
        self.connection = Connect(
                            'ora-scsp.srv.mst.edu',
                            1521,
                            os.environ['DBEAVER_USERNAME'],
                            os.environ['DBEAVER_PASSWORD'],
                            'scsp.mst.edu'
                        )
        self.connection.establish_connection() 

    def get(self):              
        order_by = ' ORDER BY BOOK_CONDITION.JACKET_CONDITION '
        
        req = {
            'jacket_condition':request.args.get("jacket_condition"),
        }
        
        where_cmds = []
        if req['jacket_condition'] != None:
            where_cmds.append(' BOOK_CONDITION.TITLE = \'{}\' '.format(req['title']))
            where_cmds.append(' BOOK_CONDITION.AUTHOR = \'{}\' '.format(req['author']))
            where_cmds.append(' BOOK_CONDITION.EDTION = \'{}\' '.format(req['edtion']))
            where_cmds.append(' BOOK_CONDITION.JACKET_CONDITION = \'{}\' '.format(req['jacket_condition']))

        command = 'SELECT TITLE, AUTHOR, EDITION, JACKET_CONDITION FROM GCWZF4.BOOK_CONDITION {} {} {}'.format('WHERE' if len(where_cmds)>0 else '','AND'.join(where_cmds), order_by)

        data = self.connection.get_query_data(
            command
        )

        jacket_conditions = []

        return_val = []
        return_code = 200

        if data != []:
            for row in data:
                jacket_conditions.append({
                    "title":row[0],
                    "author":row[1],
                    "edition":row[2],
                    "jacket_condition":row[3],
                    })

            return_val = jacket_conditions
        else:
            return_val = 'ERROR'
            return_code = 500
                    
        self.connection.close_connection()
        return return_val, return_code


    def post(self, name):
        pass
    def put(self, name):
        pass
    def delete(self, name):
        pass
