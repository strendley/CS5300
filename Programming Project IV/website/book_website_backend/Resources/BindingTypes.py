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
    'binding_type': fields.String
}

class BindingTypes(Resource):
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
        order_by = ' ORDER BY BINDING_TYPES.BINDING_TYPE '
        
        req = {
            'author':request.args.get("author"),
        }
        
        where_cmds = []
        if req['author'] != None:
            where_cmds.append(' BINDING_TYPES.BINDING_TYPE = \'{}\' '.format(req['author']))

        command = 'SELECT * FROM GCWZF4.BINDING_TYPES {} {} {}'.format('WHERE' if len(where_cmds)>0 else '','AND'.join(where_cmds), order_by)

        data = self.connection.get_query_data(
            command
        )

        binding_types = []

        return_val = []
        return_code = 200

        if data != []:
            for row in data:
                binding_types.append({"binding_type":row[0]})

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
