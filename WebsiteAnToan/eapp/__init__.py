from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from eapp.protector import output_encode

app = Flask(__name__)
app.secret_key = 'JKHGIUGYUF(*&^&*^*YTTDYFJHGH*T^&T*T&GHKJHJGH'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:bB0908650232@localhost/forumdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE'] = 10
app.add_template_filter(output_encode, 'output_encode')

db = SQLAlchemy(app=app)
login = LoginManager(app=app)