#!/usr/bin/python3
from flask import Flask 
from flask_restful import Api, Resource, reqparse, fields, request
from flask_cors import CORS
from connect import Connect
import os, pandas, debug


book_edition_fields = {
    'title': fields.String,
    'edition': fields.String,
    'isbn': fields.String,
    'pages': fields.String,
    'publish_year': fields.String,
    'notes': fields.String,
    'author': fields.String
}


class BookEditions(Resource):
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
            'edition':request.args.get("edition"),
            'title':request.args.get("title"),
        }
        
        where_cmds = []
        if req['author'] != None:
            where_cmds.append(' AUTHORS.AUTHOR = \'{}\' '.format(req['author']))
        if req['edition'] != None:
            where_cmds.append(' EDITION = \'{}\' '.format(req['edition']))
        if req['title'] != None:
            where_cmds.append(' TITLE = \'{}\' '.format(req['title']))
        
        command = 'SELECT TITLE, EDITION, AUTHORS.AUTHOR, PUBLISH_YEAR, IMAGE_PATH FROM GCWZF4.BOOK_EDITIONS JOIN GCWZF4.AUTHORS ON AUTHORS.AUTHOR = BOOK_EDITIONS.AUTHOR {} {} {}'.format('WHERE' if len(where_cmds)>0 else '','AND'.join(where_cmds), order_by)
        
        data = self.connection.get_query_data(
            command
        )

        return_val = []
        return_code = 200

        if data != []:
            books = []
            i = 0
            for row in data:
                if row[4] and ((row[2].split(' ')[0] not in row[4]) or (len(row[2].split(' ')) > 2 and row[2].split(' ')[1] not in row[4])):
                    books.append({
                        "id": i,
                        "title":row[0],
                        "edition":row[1],
                        "author": row[2],
                        "year": row[3],
                        "image_path": 'null'
                        })
                else:
                    books.append({
                        "id": i,
                        "title":row[0],
                        "edition":row[1],
                        "author": row[2],
                        "year": row[3],
                        "image_path": row[4]
                        })
                i+=1

            return_val = books
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

