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
class Years(Resource):
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
        order_by = ' ORDER BY BOOK_EDITIONS.PUBLISH_YEAR, BOOK_EDITIONS.TITLE '
        
        req = {
            'author':request.args.get("author"),
        }
        
        where_cmds = []
        if req['author'] != None:
            where_cmds.append(' BOOK_EDITIONS.AUTHOR = \'{}\' '.format(req['author']))

        command = 'SELECT BOOK_EDITIONS.PUBLISH_YEAR, BOOK_EDITIONS.TITLE FROM GCWZF4.BOOK_EDITIONS {}'.format(order_by) 

        data = self.connection.get_query_data(
            command
        )

        years = {}
        years['publish_year'] = {}

        return_val = []
        return_code = 200

        if data != []:
            for row in data:
                print(row[0])
                if row[0] not in years['publish_year']:
                    years['publish_year'][row[0]] = [row[1]]  
                else:
                    years['publish_year'][row[0]].append(row[1])
            
            return_val = years
        else:
            return_val = 'ERROR'
            return_code = 500
                    
        self.connection.close_connection()
        return return_val, return_code