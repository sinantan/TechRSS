import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__,template_folder='app/templates')
app.secret_key="rssfeed" #flash mesaj verebilmek için secret key oluşturmamız gerekiyor.
app.security_password_salt="rssfeed2"

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'teknofeed.db')

db = SQLAlchemy(app)


from app.views import *



if __name__=="__main__":
	db.create_all()
	app.run(debug=True)