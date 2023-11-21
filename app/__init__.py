from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager

s = "Admin@123"

app = Flask(__name__)
app.secret_key = '235657586DGFHJMNF4354574$#%$^%&5EF#%$^&$#$@FDGFNBCB#%$^%&^2436546587FDSGBNFM'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/bookstoredb?charset=utf8mb4" % quote(s)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE'] = 12

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
