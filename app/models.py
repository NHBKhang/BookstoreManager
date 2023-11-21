from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from app import db, app
from datetime import datetime
from flask_login import UserMixin
import enum
import hashlib


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(100),
                   default='https://www.google.com/url?sa=i&url=https%3A%2F%2Fstock.adobe.com%2Fsearch%3Fk%3Dnth&psig=AOvVaw2ikijy0zik25q-f-qDM3gL&ust=1700653615974000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCJja38aC1YIDFQAAAAAdAAAAABAE')
    active = Column(Boolean, default=True)
    description = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


class GenderType(enum.Enum):
    MALE = 1,
    FEMALE = 2


class PersonalInfo(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birthday = Column(DateTime, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(10), unique=True, nullable=False)
    gender = Column(Enum(GenderType), nullable=False, default=GenderType.MALE)
    address = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)


class UserStatus(enum.Enum):
    ACTIVE = 1,
    BANNED = 2


class UserRole(enum.Enum):
    ADMIN = 1
    USER = 2


class Account(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(str(User.last_name + User.last_name))
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    personal_info = relationship('PersonalInfo', backref='user', lazy=True)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    register_date = Column(DateTime())
    use_role = Column(Enum(UserRole), default=UserRole.USER)
    # products = relationship(Product, backref='user', lazy=True)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    birthday = Column(DateTime())
    email = Column(String(50), nullable=False)
    phone = Column(String(20))
    gender = Column(Enum(GenderType))
    address = Column(String(100), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        c1 = Category('book1')
        c2 = Category('book2')
        c3 = Category('book3')
        db.session.add_all([c1, c2, c3])
        admin = Account(name='halo', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                        user_role=UserRole.ADMIN)
        db.session.add(admin)
        db.create_all()
