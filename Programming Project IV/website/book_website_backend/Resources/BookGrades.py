#!/usr/bin/python3
from flask import Flask 
from flask_restful import Api, Resource, reqparse, fields, request
from flask_cors import CORS
from connect import Connect
import os, pandas, debug

app = Flask(__name__)
api = Api(app)
CORS(app)

grades_fields = {
    'grades': fields.String
}

class BookGrades(Resource):
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
        order_by = ' ORDER BY BOOK_GRADE.BOOK_GRADE '
        
        req = {
            'grade':request.args.get("grade"),
        }
        
        where_cmds = []
        if req['grade'] != None:
            where_cmds.append(' BOOK_GRADE.TITLE = \'{}\' '.format(req['title']))
            where_cmds.append(' BOOK_GRADE.AUTHOR = \'{}\' '.format(req['author']))
            where_cmds.append(' BOOK_GRADE.EDTION = \'{}\' '.format(req['edtion']))
            where_cmds.append(' BOOK_GRADE.BOOK_GRADE = \'{}\' '.format(req['grade']))

        command = 'SELECT TITLE, AUTHOR, EDITION, BOOK_GRADE FROM GCWZF4.BOOK_GRADE {} {} {}'.format('WHERE' if len(where_cmds)>0 else '','AND'.join(where_cmds), order_by)

        data = self.connection.get_query_data(
            command
        )

        grades = []

        return_val = []
        return_code = 200

        if data != []:
            for row in data:
                grades.append({
                    "title":row[0],
                    "author":row[1],
                    "edition":row[2],
                    "grade":row[3],
                    })

            return_val = grades
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
