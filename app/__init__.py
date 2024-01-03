from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask import Flask

app = Flask(__name__)

s = "Admin@123"
s1 = "Abc111!"

app.secret_key = '235657586DGFHJMNF4354574$#%$^%&5EF#%$^&$#$@FDGFNBCB#%$^%&^2436546587FDSGBNFM'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/bookstoredb?charset=utf8mb4" % quote(s1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE'] = 9
app.config['CART_KEY'] = 'cart'
app.config['SALES_KEY'] = 'sales_cart'

db = SQLAlchemy(app=app)
login = LoginManager(app=app)