from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from app import db, app
from datetime import datetime
from flask_login import UserMixin
import enum


# class Category(db.Model):
#     pass
#
#
# class Product(db.Model):
#     pass


# class GenderType(enum.Enum):
#     MALE = 1,
#     FEMALE = 2
#
#
# class PersonalInfo(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     first_name = Column(String(50), nullable=False)
#     last_name = Column(String(50), nullable=False)
#     birthday = Column(DateTime, nullable=False)
#     email = Column(String(50), unique=True, nullable=False)
#     phone = Column(String(10), unique=True, nullable=False)
#     gender = Column(Enum(GenderType), nullable=False, default=GenderType.MALE)
#     address = Column(String(100), nullable=False)
#     user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
#
#
# class UserStatus(enum.Enum):
#     ACTIVE = 1,
#     BANNED = 2
#
#
# class User(db.Model, UserMixin):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String(50), nullable=False)
#     password = Column(String(50), nullable=False)
#     personal_info = relationship('PersonalInfo', backref='user', lazy=True)
#     status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    # use_role = Column(Enum(UserRole), default=UserRole.USER)
    # products = relationship(Product, backref='user', lazy=True)


if __name__ == '__main__':
    with app.app_context():
        pass
        #db.create_all()
