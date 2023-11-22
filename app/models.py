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
    books = relationship('Book', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Author(db.Model):
    __tablename__ = 'author'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    books = relationship('Book_Author', backref='author', lazy=True)

    def __str__(self):
        return self.name


class Inventory(db.Model):
    __tablename__ = 'inventory'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)

    def __str__(self):
        return self.name


class Book(db.Model):
    __tablename__ = 'book'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(100),
                   default='https://www.google.com/url?sa=i&url=https%3A%2F%2Fstock.adobe.com%2Fsearch%3Fk%3Dnth&psig=AOvVaw2ikijy0zik25q-f-qDM3gL&ust=1700653615974000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCJja38aC1YIDFQAAAAAdAAAAABAE')
    active = Column(Boolean, default=True)
    description = Column(String(255), nullable=False)
    authors = relationship("Book_Author", backref='book', lazy=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    inventories = relationship("Book_Inventory", backref='book', lazy=True)

    def __str__(self):
        return self.name


class Book_Author(db.Model):
    __tablename__ = 'book_author'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)
    publisher_date = Column(DateTime, nullable=False)


class Book_Inventory(db.Model):
    __tablename__ = 'book_inventory'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    inventory_id = Column(Integer, ForeignKey(Inventory.id), nullable=False, default=1)
    quantity = Column(Integer, nullable=False)
    added_date = Column(DateTime, nullable=False, default=datetime.now())


class GenderType(enum.Enum):
    MALE = 1,
    FEMALE = 2


class AccountStatus(enum.Enum):
    ACTIVE = 1,
    BANNED = 2


class AdminRole(enum.Enum):
    OWNER = 1


class Account(db.Model, UserMixin):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    avatar = Column(String(255), nullable=False,
                    default='https://e7.pngegg.com/pngimages/799/987/png-clipart-computer-icons-avatar-icon-design-avatar-heroes-computer-wallpaper-thumbnail.png')
    register_date = Column(DateTime, default=datetime.now())
    last_login = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Admin(Account):
    __tablename__ = 'admin'
    __table_args__ = {'extend_existing': True}

    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(Enum(AdminRole), default=AdminRole.OWNER)


class User(Account):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birthday = Column(DateTime, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(12), unique=True, nullable=False)
    gender = Column(Enum(GenderType), nullable=False, default=GenderType.MALE)
    address = Column(String(100), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # import hashlib
        # admin = Admin(username='admin', password=hashlib.md5("123456".encode('utf-8')).hexdigest(), name='admin',
        #                      email='admin@gmail.com')
        # db.session.add_all([admin])
        # db.session.commit()

        # category = Category(name='Viễn Tưởng')
        # db.session.add_all([category])
        # db.session.commit()

        # inventory = Inventory(name='Kho 1')
        # db.session.add_all([inventory])
        # db.session.commit()

        # author = Author(name='Vincent A Kennard')
        # db.session.add_all([author])
        # db.session.commit()

        # b1 = Book(name='The Wolf Chronicles', price=450000,
        #                  image='https://m.media-amazon.com/images/I/61ypicJcl+L._SY342_.jpg',
        #                  description='Biên niên sử sói Phần 1 Tinh thần của một con sói.', category_id=1)
        # db.session.add_all([b1])
        # db.session.commit()

        # ba1 = Book_Author(book_id=1, author_id=1, publisher_date=datetime.strptime('07/09/2007', '%d/%m/%Y'))
        # db.session.add_all([ba1])
        # db.session.commit()

        # bi1 = Book_Inventory(book_id=1, inventory_id=1, quantity=100)
        # db.session.add_all([bi1])
        # db.session.commit()
