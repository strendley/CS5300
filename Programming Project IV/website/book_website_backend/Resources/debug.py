import os

class Debug:
    def __init__(self):
        pass
    def log(self,s):
        if 'DEBUG' in os.environ.keys() and os.environ['DEBUG'] == 'True':
            print(s)