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
class AuthorBooks(Resource):
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

        command = 'SELECT AUTHORS.AUTHOR, AUTHORS.IMAGE_PATH, TITLE, PUBLISH_YEAR FROM GCWZF4.BOOK_EDITIONS JOIN GCWZF4.AUTHORS ON AUTHORS.AUTHOR = BOOK_EDITIONS.AUTHOR {} {} {}'.format('WHERE' if len(where_cmds)>0 else '','AND'.join(where_cmds), order_by)
        print(command)
        data = self.connection.get_query_data(
            command
        )

        authors = {}

        return_val = []
        return_code = 200

        if data != []:
            authors['author'] = data[0][0]
            authors['image_path'] = data[0][1]
            authors['books'] = []
            for row in data:
                authors['books'].append({
                    "title":row[2],
                    "publish_year":row[3]    
                })

            return_val = authors
        else:
            return_val = 'ERROR'
            return_code = 500
                    
        self.connection.close_connection()
        return return_val, return_code