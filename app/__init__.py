from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask import Flask
from flask_mail import Mail
from app.otp import MailOTP
import base64
import secrets

app = Flask(__name__)

s1 = "Abc111!"

# project settings
app.secret_key = '235657586DGFHJMNF4354574$#%$^%&5EF#%$^&$#$@FDGFNBCB#%$^%&^2436546587FDSGBNFM'

# database settings
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/bookstoredb?charset=utf8mb4" % quote(s1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# page settings
app.config['PAGE_SIZE'] = 9
app.config['CART_KEY'] = 'cart'
app.config['SALES_KEY'] = 'sales_cart'

# mail server settings
app.config['MAIL_SERVER'] = 'smtp.ethereal.email'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'gregg.heidenreich79@ethereal.email'
app.config['MAIL_PASSWORD'] = 'yKQ6p38z7FZqcQWtd8'
app.config['MAIL_SECRET_KEY'] = base64.b32encode(secrets.token_bytes(16)).decode('utf-8')

# vnpay settings
app.config['VNP_TMN_CODE'] = 'LP7Z4P3V'
app.config['VNP_HASH_SECRET'] = 'JOHVXEOHNQHDOMXMBRCQLQQCUVTWKNGM'
app.config['VNP_URL'] = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'
app.config['VNP_IP_ADDRESS'] = "127.0.0.1"
app.config['VNP_CURRENCY_CODE'] = 'VND'
app.config['VNP_VERSION'] = '2.1.0'
app.config['VNP_COMMAND'] = 'pay'

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
mail = Mail(app=app)
otp = MailOTP()
