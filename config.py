import os
DEBUG = True
CSRF_ENABLED = True


SECRET_KEY= os.urandom(24)
# mysql+pymysql://username:password@server/db
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'zdh1989'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'flaskdb'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST
                                             ,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
