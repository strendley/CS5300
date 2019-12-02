#!/usr/bin/python3
from flask import Flask 
from flask_restful import Api, Resource, reqparse, fields, request
from flask_cors import CORS
from connect import Connect
import os, pandas, debug

app = Flask(__name__)
api = Api(app)
CORS(app)

debugger = debug.Debug()

author_fields = {
    'author': fields.String
}

class AddBook(Resource):
    def __init__(self):
        self.connection = Connect(
                            'ora-scsp.srv.mst.edu',
                            1521,
                            os.environ['DBEAVER_USERNAME'],
                            os.environ['DBEAVER_PASSWORD'],
                            'scsp.mst.edu'
                        )
        self.connection.establish_connection() 

    def post(self):          
        req = {
            'author':request.args.get("author"),
            'title':request.args.get("title"),
            'edition':request.args.get("edition"),
            'img_path':request.args.get("img_path"),
            'gutenberg_path':request.args.get("gutenberg_path"),
            'publisher':request.args.get("publisher"),
            'notes':request.args.get("notes"),
            'isbn':request.args.get("isbn"),
            'publish_year':request.args.get("publish_year"),
            'pages':request.args.get("pages"),
            'book_grade':request.args.get('book_grade'),
            'binding_type':request.args.get("binding_type"),
            'jacket_condition':request.args.get("jacket_condition")
        }

        if  req['author'] == None or \
            req['title'] == None or \
            req['edition'] == None:
            return_val = 'ERROR: author or title or edition is missing and must be present'
            return_code = 400
        else:
            authors = []
            jacket_conditions = []
            book_grades = []
            publishers = []
            book_editions = []

            # check if author is in the database if not we'll add the author
            command = 'SELECT AUTHOR FROM GCWZF4.AUTHORS WHERE AUTHOR = \'{}\''.format(req['author'])
            authors = self.connection.get_query_data(command)

            if authors == []:
                columns = ','.join([
                    x for x in [
                        'AUTHOR',
                        'IMAGE_PATH' if req['img_path'] != None else 'NULL'
                    ] if x != 'NULL'
                ])
                values = '\',\''.join([
                    x for x in [
                        req['author'],
                        req['img_path'] if req['img_path'] != None else 'NULL'
                    ] if x != 'NULL'
                ])
                
                command = 'INSERT INTO GCWZF4.AUTHORS({}) \nVALUES (\'{}\')'.format(columns,values)
                debugger.log(command)                
                self.connection.run_command(command)

            # check if book_edition is in the database if not we'll add the book_edition
            command = 'SELECT TITLE, EDITION, AUTHOR FROM GCWZF4.BOOK_EDITIONS WHERE  TITLE = \'{}\' AND AUTHOR = \'{}\' AND EDITION = \'{}\''.format( req['title'], req['author'], req['edition'] )
            book_editions = self.connection.get_query_data(command)

            if book_editions == []:
                columns = ','.join([x for x in [
                        'TITLE',
                        'EDITION',
                        'AUTHOR',
                        'ISBN' if req['isbn'] != None else 'NULL',
                        'PAGES' if req['pages'] != None else 'NULL',
                        'PUBLISH_YEAR' if req['publish_year'] != None else 'NULL',
                        'NOTES' if req['notes'] != None else 'NULL',
                        'GUTENBERG_PATH' if req['gutenberg_path'] != None else 'NULL'] 
                        if x != 'NULL'])
                values = '\',\''.join([x for x in [
                        req['title'],
                        req['edition'],
                        req['author'],
                        req['isbn'] if req['isbn'] != None else 'NULL',
                        req['pages'] if req['pages'] != None else 'NULL',
                        req['publish_year'] if req['publish_year'] != None else 'NULL',
                        req['notes'] if req['notes'] != None else 'NULL',
                        req['gutenberg_path'] if req['gutenberg_path'] != None else 'NULL'] 
                        if x != 'NULL'])

                command = 'INSERT INTO GCWZF4.BOOK_EDITIONS({}) \nVALUES (\'{}\')'.format(columns, values) 
                debugger.log(command)               
                self.connection.run_command(command)         

            if req['jacket_condition'] != None:
                # check if jacket_condition is in the database if not we'll add the jacket_condition
                command = 'SELECT JACKET_CONDITION FROM GCWZF4.JACKET_CONDITIONS WHERE JACKET_CONDITION = \'{}\''.format(req['jacket_condition'])
                jacket_conditions = self.connection.get_query_data(command)
                # debugger.log(command)

                if jacket_conditions == []:
                    command = 'INSERT INTO GCWZF4.JACKET_CONDITIONS(JACKET_CONDITION) \nVALUES (\'{}\')'.format(req['jacket_condition'])
                    debugger.log(command)
                    self.connection.run_command(command)
                    
                    command = 'INSERT INTO GCWZF4.BOOK_CONDITION(TITLE, AUTHOR, EDITION, JACKET_CONDITION) \nVALUES (\'{}\')'.format('\',\''.join([req['title'],req['author'],req['edition'],req['jacket_condition']]))
                    debugger.log(command)
                    self.connection.run_command(command)

            if req['book_grade'] != None:
                # check if book_grade is in the database if not we'll add the book_grade
                command = 'SELECT BOOK_GRADE FROM GCWZF4.GRADE WHERE BOOK_GRADE = \'{}\''.format(req['book_grade'])
                book_grades = self.connection.get_query_data(command)
                # debugger.log(command)

                if book_grades == []:
                    command = 'INSERT INTO GCWZF4.GRADE(BOOK_GRADE) \nVALUES (\'{}\')'.format(req['book_grade'])
                    debugger.log(command)
                    self.connection.run_command(command)

                    command = 'INSERT INTO GCWZF4.BOOK_GRADE(TITLE, AUTHOR, EDITION, BOOK_GRADE) \nVALUES (\'{}\')'.format('\',\''.join([req['title'],req['author'],req['edition'],req['book_grade']]))
                    debugger.log(command)
                    self.connection.run_command(command)

            if req['publisher'] != None:
                # check if publisher is in the database if not we'll add the publisher
                command = 'SELECT PUBLISHER FROM GCWZF4.PUBLISHERS WHERE PUBLISHER = \'{}\''.format(req['publisher'])
                publishers = self.connection.get_query_data(command)

                if publishers == []:
                    command = 'INSERT INTO GCWZF4.PUBLISHERS(PUBLISHER) \nVALUES (\'{}\')'.format(req['publisher'])
                    # debugger.log(command)
                    self.connection.run_command(command)
                    
                    command = 'INSERT INTO GCWZF4.PUBLISHER_BOOKS(TITLE, AUTHOR, EDITION, PUBLISHER) \nVALUES (\'{}\')'.format('\',\''.join([req['title'],req['author'],req['edition'],req['publisher']]))
                    # debugger.log(command)
                    self.connection.run_command(command)


            if req['binding_type'] != None:
                # check if binding_type is in the database if not we'll add the binding_type
                command = 'SELECT BINDING_TYPE FROM GCWZF4.BINDING_TYPES WHERE BINDING_TYPE = \'{}\''.format(req['binding_type'])
                binding_types = self.connection.get_query_data(command)

                if binding_types == []:
                    command = 'INSERT INTO GCWZF4.BINDING_TYPES(BINDING_TYPE) \nVALUES (\'{}\')'.format(req['binding_type'])
                    # debugger.log(command)
                    self.connection.run_command(command)
                    command = 'INSERT INTO GCWZF4.BOOK_BINDING_TYPES(TITLE, AUTHOR, EDITION, BINDING_TYPE) \nVALUES (\'{}\')'.format('\',\''.join([req['title'],req['author'],req['edition'],req['binding_type']]))
                    # debugger.log(command)
                    self.connection.run_command(command)

        return_val = 'Success'
        return_code = 200

        self.connection.close_connection()
        return return_val, return_code