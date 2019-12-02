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

class PublisherBooks(Resource):
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
        order_by = ' ORDER BY PUBLISHER_BOOKS.PUBLISHER '
        
        req = {
            'publisher':request.args.get("publisher"),
        }
        
        where_cmds = []
        if req['publisher'] != None:
            where_cmds.append(' PUBLISHER_BOOKS.TITLE = \'{}\' '.format(req['title']))
            where_cmds.append(' PUBLISHER_BOOKS.AUTHOR = \'{}\' '.format(req['author']))
            where_cmds.append(' PUBLISHER_BOOKS.EDTION = \'{}\' '.format(req['edtion']))
            where_cmds.append(' PUBLISHER_BOOKS.PUBLISHER = \'{}\' '.format(req['publisher']))

        command = 'SELECT TITLE, AUTHOR, EDITION, PUBLISHER FROM GCWZF4.PUBLISHER_BOOKS {} {} {}'.format('WHERE' if len(where_cmds)>0 else '','AND'.join(where_cmds), order_by)

        data = self.connection.get_query_data(
            command
        )

        publishers = []

        return_val = []
        return_code = 200

        if data != []:
            for row in data:
                publishers.append({
                    "title":row[0],
                    "author":row[1],
                    "edition":row[2],
                    "publisher":row[3],
                    })

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
