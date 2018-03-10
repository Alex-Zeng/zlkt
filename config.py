import os
DEBUG = True
CSRF_ENABLED = True


SECRET_KEY= os.urandom(24)
# mysql+pymysql://username:password@server/db
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'windows'
HOST = '119.29.179.53'
PORT = '3306'
DATABASE = 'flask_db'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST
                                             ,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
