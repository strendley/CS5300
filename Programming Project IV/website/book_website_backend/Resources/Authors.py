#!/usr/bin/python3
from flask import Flask 
from flask_restful import Api, Resource, reqparse, fields, request
from flask_cors import CORS
from connect import Connect
import os, pandas, debug

app = Flask(__name__)
api = Api(app)
CORS(app)

author_fields = {
    'author': fields.String
}
class Authors(Resource):
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
        order_by = ' ORDER BY AUTHORS.AUTHOR '
        
        req = {
            'author':request.args.get("author"),
        }
        
        where_cmds = []
        if req['author'] != None:
            where_cmds.append(' AUTHORS.AUTHOR = \'{}\' '.format(req['author']))

        command = 'SELECT * FROM GCWZF4.AUTHORS {} {} {}'.format('WHERE' if len(where_cmds)>0 else '','AND'.join(where_cmds), order_by)
        
        data = self.connection.get_query_data(
            command
        )

        authors = []

        return_val = []
        return_code = 200

        if data != []:
            for row in data:
                authors.append({
                    "author":row[0],
                    "image_path":row[1]})

            return_val = authors
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

