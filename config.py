import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_AUTH', 'mysql+mysqlconnector://gr_apps:#granderecife_apps#@localhost/gr_auth')
    SQLALCHEMY_TRACK_MODIFICATIONS = False