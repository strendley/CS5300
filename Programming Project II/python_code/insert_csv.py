#!/usr/bin/python3
import pandas as pd, sys, csv, codecs, numpy as np
from connect import Connect

filein = sys.argv[1]

# dbeaver = Connect(
#             'ora-scsp.srv.mst.edu',
#             1521,
#             'username',#<- edit this
#             'password',#<- edit this
#             'scsp.mst.edu'
#         )
df = pd.read_csv(filein)
df['EDITION'] = df.EDITION.replace(np.nan, '0')
df['AUTHOR'] = df.AUTHOR.replace(regex=True, to_replace=r'[\'-()+.,*]',value='')
df['PUBLISHER'] = df.PUBLISHER.replace(regex=True, to_replace=r'[\'-()+.,*]',value='')
df['TITLE'] = df.TITLE.replace(regex=True, to_replace=r'[\'-()+.,*]',value='')

# create arrays to populate the single attribute tables
publishers = df.PUBLISHER.unique()
authors = df.AUTHOR.unique()
jacket_conditions = df.JACKET_CONDITION.unique()
binding_types = df.BINDING_TYPE.unique()
grades = df.BOOK_GRADE.unique()
bk_types = df.BOOK_TYPE.unique()

#remove all null values from the arrays
publishers = publishers[~pd.isnull(publishers)]
authors = authors[~pd.isnull(authors)]
jacket_conditions = jacket_conditions[~pd.isnull(jacket_conditions)]
binding_types = binding_types[~pd.isnull(binding_types)]
grades = grades[~pd.isnull(grades)]
bk_types = bk_types[~pd.isnull(bk_types)]

#               0       1       2           3           4                   5               6           7       8           9           10      11
col_names = ['AUTHOR','TITLE','EDITION','BOOK_GRADE','JACKET_CONDITION','PUBLISHER','BINDING_TYPE','BOOK_TYPE','ISBN ','PUBLISH_YEAR','PAGES','NOTES']

# all these dataframes should have unique rows, duplicates need to be droped
book_binding_types = df.drop(['BOOK_GRADE','JACKET_CONDITION','PUBLISHER','BOOK_TYPE','ISBN ','PUBLISH_YEAR','PAGES','NOTES'],axis=1)
book_binding_types = book_binding_types.drop_duplicates()
book_binding_types.dropna()

book_condtions = df.drop(['BOOK_GRADE','PUBLISHER','BINDING_TYPE','BOOK_TYPE','ISBN ','PUBLISH_YEAR','PAGES','NOTES'], axis=1)
book_condtions = book_condtions.drop_duplicates()
book_condtions.dropna()

book_types = df.drop(['BOOK_GRADE','JACKET_CONDITION','PUBLISHER','BINDING_TYPE','ISBN ','PUBLISH_YEAR','PAGES','NOTES'], axis=1)
book_types = book_types.drop_duplicates()
book_types.dropna()
print(book_types.head())
publisher_books = df.drop(['BOOK_GRADE','JACKET_CONDITION','BINDING_TYPE','BOOK_TYPE','ISBN ','PUBLISH_YEAR','PAGES','NOTES'],axis=1)
publisher_books = publisher_books.drop_duplicates()
publisher_books.dropna()

book_grades = df.drop(['JACKET_CONDITION','PUBLISHER','BINDING_TYPE','BOOK_TYPE','ISBN ','PUBLISH_YEAR','PAGES','NOTES'],axis=1)
book_grades = book_grades.drop_duplicates()
book_grades.dropna()

book_editions = df.drop(['BOOK_GRADE','PUBLISHER','JACKET_CONDITION','BINDING_TYPE','BOOK_TYPE'],axis=1)
book_editions = book_editions.drop_duplicates(['AUTHOR','TITLE','EDITION'])

# storing everything in a text file
with open('out.txt','w') as fout:
    # fout.write(command)

    # Insert into the authors table
    command = ''
    for author in authors:
        command += '\nINSERT INTO GCWZF4.AUTHORS\n    VALUES(\'{}\');'.format(author)
    # command += '\nSELECT * FROM DUAL;'
    fout.write(command)
    fout.write('\n')

    # Insert into the publishers table
    command = ''
    for publisher in publishers:
        command += '\nINSERT INTO GCWZF4.PUBLISHERS\n    VALUES(\'{}\');'.format(publisher)
    # command += '\nSELECT * FROM DUAL;'
    fout.write(command)
    fout.write('\n')

    # Insert into jacket_conditions
    command = ''
    for condition in jacket_conditions:
        command += '\nINSERT INTO GCWZF4.JACKET_CONDITIONS\n    VALUES(\'{}\');'.format(condition)
    # command += '\nSELECT * FROM DUAL;'
    fout.write(command)
    fout.write('\n')

    # Insert into binding_types table
    command = ''
    for binding in binding_types:
        command += '\nINSERT INTO GCWZF4.BINDING_TYPES\n    VALUES(\'{}\');'.format(binding)
    # command += '\nSELECT * FROM DUAL;'
    fout.write(command)
    fout.write('\n')
    
    # Insert into the Grade table
    command = ''
    for grade in grades:
        command += '\nINSERT INTO GCWZF4.GRADE\n    VALUES(\'{}\');'.format(grade)
    # command += '\nSELECT * FROM DUAL;'
    fout.write(command)
    fout.write('\n')

    # Insert into the book_type table
    command = ''
    for _type in bk_types:
        command += '\nINSERT INTO GCWZF4.TYPES\n    VALUES(\'{}\');'.format(_type)
        print(_type)

    # command += '\nSELECT * FROM DUAL;'
    fout.write(command)
    fout.write('\n')


    # Insert into the book_editions table
    header = ','.join(book_editions.columns)
    command = ''
    for row in book_editions.values:
        row = [str(x) for x in row]
        command += '\nINSERT INTO GCWZF4.BOOK_EDITIONS({})\n   VALUES (\'{}\');'.format(
                header,
                '\',\''.join(row)
        )
    # command += '\nSELECT * FROM DUAL;'
    fout.write(command)
    fout.write('\n')
    
    # Insert into the book_binding_types table
    header = ','.join(book_binding_types.columns)
    command = ''
    for row in book_binding_types.values:
        row = [str(x) for x in row]
        command += '\nINSERT INTO GCWZF4.BOOK_BINDING_TYPES({})\n   VALUES (\'{}\');'.format(
                header,
                '\',\''.join(row)
        )
    # command += '\nSELECT * FROM DUAL;'
    fout.write(command)
    fout.write('\n')

    # Insert into the book_binding_types table
    header = ','.join(book_condtions.columns)
    command = ''
    for row in book_condtions.values:
        row = [str(x) for x in row]
        command += '\nINSERT INTO GCWZF4.BOOK_CONDITION({})\n   VALUES (\'{}\');'.format(
                header,
                '\',\''.join(row)
        )
    # command += '\nSELECT * FROM DUAL;'
    fout.write(command)
    fout.write('\n')

    # Insert into the book_binding_types table
    header = ','.join(book_types.columns)
    command = ''
    for row in book_types.values:
        row = [str(x) for x in row]
        command += '\nINSERT INTO GCWZF4.BOOK_TYPE({})\n   VALUES (\'{}\');'.format(
                header,
                '\',\''.join(row)
        )
    # command += '\nSELECT * FROM DUAL;'
    fout.write(command)
    fout.write('\n')

    # Insert into the book_binding_types table
    header = ','.join(publisher_books.columns)
    command = ''
    for row in publisher_books.values:
        row = [str(x) for x in row]
        command += '\nINSERT INTO GCWZF4.PUBLISHER_BOOKS({})\n   VALUES (\'{}\');'.format(
                header,
                '\',\''.join(row)
        )
    # command += '\nSELECT * FROM DUAL;'
    fout.write(command)
    fout.write('\n')

    # Insert into the book_binding_types table
    header = ','.join(book_grades.columns)
    command = ''
    for row in book_grades.values:
        row = [str(x) for x in row]
        command += '\nINSERT INTO GCWZF4.BOOK_GRADE({})\n   VALUES (\'{}\');'.format(
                header,
                '\',\''.join(row)
        )
    # command += '\nSELECT * FROM DUAL;'
    fout.write(command)
    fout.write('\n')

# # # dbeaver.establish_connection()
# # # dbeaver.run_command(command)
# # # dbeaver.close_connection()
