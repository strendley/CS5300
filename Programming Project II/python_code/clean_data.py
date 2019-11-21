#!/usr/bin/python3
import cx_Oracle, pandas as pd, sys, csv, codecs

filein = sys.argv[1]

def get_file_contents(filein):
    header = []
    data = []
    i = 0
    with codecs.open(filein, encoding='utf-8', errors='ignore') as fin:
        reader = csv.reader(fin)
        data = [r for r in reader if r[0] != '' and r[1] != '' and r[2] != '']
        header = data.pop(0)
        header = [x.upper() for x in header]
        fin.close()

    header[3] = 'BOOK_GRADE'
    header[4] = 'JACKET_CONDITION'
    header[5] = 'BINDING_TYPE'
    header[6] = 'BOOK_TYPE'
    header[8] = 'PUBLISHER_YEAR'
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == '':
                data[i][j] = 'NULL'
            if '\'' in data[i][j]:
                data[i][j] = data[i][j].replace('\'','')

    return pd.DataFrame(data=data, columns=header)

df = get_file_contents(filein)
df['PAGES'] = df['PAGES'].str.replace('[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+-.!@#$%^&*() ]','')
df['EDITION'] = df['EDITION'].str.replace('[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+-.!@#$%^&*() ]','')
df['ISBN '] = df['ISBN '].str.replace('[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+-.!@#$%^&*() ]','')

for col in df.columns:
    df.loc[df[col] == '', col] = 'NULL'
df = df.replace('????','NULL')
df = df.drop_duplicates()
df.to_csv('cleaned_data.csv', index=None)

