#!/usr/bin/python3
from flask import Flask 
from flask_restful import Api, Resource, reqparse, fields, request
from flask_cors import CORS
from connect import Connect
import os, pandas, debug

app = Flask(__name__)
api = Api(app)
CORS(app)

publishers_fields = {
    'publishers': fields.String
}

class Publishers(Resource):
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
        order_by = ' ORDER BY PUBLISHERS.PUBLISHER '
        
        req = {
            'publisher':request.args.get("publisher"),
        }
        
        where_cmds = []
        if req['publisher'] != None:
            where_cmds.append(' PUBLISHERS.PUBLISHER = \'{}\' '.format(req['publisher']))

        command = 'SELECT PUBLISHER FROM GCWZF4.PUBLISHERS {} {} {}'.format('WHERE' if len(where_cmds)>0 else '','AND'.join(where_cmds), order_by)

        data = self.connection.get_query_data(
            command
        )

        publishers = []

        return_val = []
        return_code = 200

        if data != []:
            for row in data:
                publishers.append({"publisher":row[0]})

            return_val = publishers
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
