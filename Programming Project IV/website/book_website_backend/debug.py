import os

class Debug:
    def log(self,s):
        if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'True':
            print(s)