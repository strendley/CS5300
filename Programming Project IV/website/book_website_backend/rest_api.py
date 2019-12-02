#!/usr/bin/python3
from flask import Flask 
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from connect import Connect
import os, pandas, debug
from Resources.Authors import Authors
from Resources.BookEditions import BookEditions
from Resources.Grades import Grades
from Resources.BindingTypes import BindingTypes
from Resources.JacketConditions import JacketConditions
from Resources.Publishers import Publishers
from Resources.AuthorBooks import AuthorBooks
from Resources.Years import Years
from Resources.BookBindingTypes import BookBindingTypes
from Resources.BookConditions import BookConditions
from Resources.BookGrades import BookGrades
from Resources.PublisherBooks import PublisherBooks
from Resources.AddBook import AddBook

app = Flask(__name__)
api = Api(app)
CORS(app)

# Resource that are currently avalible for use
# you're able to add parameters to the url for specific querying
# example:
# http://localhost:5000/book_editions?author=Hamilton Donald&edition=0&title=The Intimidators
# params
#   author  -> string
#   edition -> string
#   title   -> string

# generalized queries for major tables
api.add_resource(Authors, "/author")

api.add_resource(BookEditions, "/book_editions")

api.add_resource(Grades, "/grade")

api.add_resource(BindingTypes, "/binding_type")

api.add_resource(JacketConditions, "/jacket_condition")

api.add_resource(Publishers, "/publisher")

api.add_resource(BookBindingTypes, '/book_binding_types')

api.add_resource(BookConditions, '/book_conditions')

api.add_resource(BookGrades, '/book_grades')

api.add_resource(PublisherBooks, '/publisher_books')
# end of genrealized queries

# api for authors page
api.add_resource(AuthorBooks, "/author_books")

# api for years page
api.add_resource(Years, "/years")


# api for addBook page
api.add_resource(AddBook, "/add_book")

app.run(debug=True)
