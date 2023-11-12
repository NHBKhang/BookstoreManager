from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

s = 'Admin@123'
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/bookstoredb?charset=utf8mb4" % quote("Abc111!")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)
