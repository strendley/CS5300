#!/usr/bin/python3
from flask import Flask 
from flask_restful import Api, Resource, reqparse, fields, request
from flask_cors import CORS
from connect import Connect
import os, pandas, debug

app = Flask(__name__)
api = Api(app)
CORS(app)

binding_types_fields = {
    'binding_types': fields.String
}

class BookBindingTypes(Resource):
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
        order_by = ' ORDER BY BOOK_BINDING_TYPES.BINDING_TYPE '
        
        req = {
            'binding_type':request.args.get("binding_type"),
        }
        
        where_cmds = []
        if req['binding_type'] != None:
            where_cmds.append(' BOOK_BINDING_TYPES.TITLE = \'{}\' '.format(req['title']))
            where_cmds.append(' BOOK_BINDING_TYPES.AUTHOR = \'{}\' '.format(req['author']))
            where_cmds.append(' BOOK_BINDING_TYPES.EDTION = \'{}\' '.format(req['edtion']))
            where_cmds.append(' BOOK_BINDING_TYPES.BINDING_TYPE = \'{}\' '.format(req['binding_type']))

        command = 'SELECT TITLE, AUTHOR, EDITION, BINDING_TYPE FROM GCWZF4.BOOK_BINDING_TYPES {} {} {}'.format('WHERE' if len(where_cmds)>0 else '','AND'.join(where_cmds), order_by)

        data = self.connection.get_query_data(
            command
        )

        binding_types = []

        return_val = []
        return_code = 200

        if data != []:
            for row in data:
                binding_types.append({
                    "title":row[0],
                    "author":row[1],
                    "edition":row[2],
                    "binding_type":row[3],
                    })

            return_val = binding_types
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
