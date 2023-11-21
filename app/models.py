from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from app import db, app
from datetime import datetime
from flask_login import UserMixin
import enum


class Category(db.Model):
    __tablename__ = 'category'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Author(db.Model):
    __tablename__ = 'author'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    __tablename__ = 'product'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(100),
                   default='https://www.google.com/url?sa=i&url=https%3A%2F%2Fstock.adobe.com%2Fsearch%3Fk%3Dnth&psig=AOvVaw2ikijy0zik25q-f-qDM3gL&ust=1700653615974000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCJja38aC1YIDFQAAAAAdAAAAABAE')
    active = Column(Boolean, default=True)
    description = Column(String(100), nullable=False)
    author_id = Column(Integer, ForeignKey(author.id), nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


class GenderType(enum.Enum):
    MALE = 1,
    FEMALE = 2


class AccountStatus(enum.Enum):
    ACTIVE = 1,
    BANNED = 2


class Account(db.Model, UserMixin):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    register_date = Column(DateTime, nullable=False, default=datetime.now())
    login_date = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())


class AdminRole(enum.Enum):
    OWNER = 1


class Administrator(Account):
    __tablename__ = 'admin'
    __table_args__ = {'extend_existing': True}

    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(Enum(AdminRole), nullable=False, default=AdminRole.OWNER)

    def __str__(self):
        return self.name


class User(Account):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birthday = Column(DateTime, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(12), unique=True, nullable=False)
    gender = Column(Enum(GenderType), nullable=False, default=GenderType.MALE)
    address = Column(String(150), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
