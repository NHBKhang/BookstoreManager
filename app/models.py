from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from app import db, app
from app.data import *
from datetime import datetime
from flask_login import UserMixin
import enum


class GenderType(enum.Enum):
    MALE = 1
    FEMALE = 2

    def __val__(self):
        return str(self.value)

    def __str__(self):
        return str(self.name)


class AccountStatus(enum.Enum):
    ACTIVE = 1
    BANNED = 2


class AdminRole(enum.Enum):
    OWNER = 1


class CustomerType(enum.Enum):
    GUEST = 1
    LOYAL = 2


class StaffJobTitle(enum.Enum):
    SALE = 1
    SHIPPING = 2


class OrderStatus(enum.Enum):
    PENDING = [1, 'bg-info']
    APPROVED = [2, 'bg-primary']
    REJECTED = [3, 'bg-danger']
    SHIPPING = [4, 'bg-info']
    RECEIVED = [5, 'bg-success']
    CANCELLED = [6, 'bg-danger']


class Category(db.Model):
    __tablename__ = 'category'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    books = relationship('Book_Category', backref='category', lazy=True)

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
    books = relationship('Book_Inventory', backref='inventory', lazy=True)

    def __str__(self):
        return self.name


class Book(db.Model):
    __tablename__ = 'book'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    price = Column(Integer, default=0)
    image = Column(String(255),
                   default='https://www.google.com/url?sa=i&url=https%3A%2F%2Fstock.adobe.com%2Fsearch%3Fk%3Dnth&psig=AOvVaw2ikijy0zik25q-f-qDM3gL&ust=1700653615974000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCJja38aC1YIDFQAAAAAdAAAAABAE')
    active = Column(Boolean, default=True)
    description = Column(String(512), nullable=False)
    published_date = Column(DateTime, nullable=False)
    categories = relationship("Book_Category", backref='book')
    authors = relationship("Book_Author", backref='book', lazy=True)
    inventories = relationship("Book_Inventory", backref='book', lazy=True)
    orders = relationship("OrderDetails", backref='book', lazy=True)
    receipts = relationship("ReceiptDetails", backref='book', lazy=True)

    def __str__(self):
        return self.name


class Book_Category(db.Model):
    __tablename__ = 'book_category'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return Category.query.get(self.category_id).name


class Book_Author(db.Model):
    __tablename__ = 'book_author'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)

    def __str__(self):
        return Author.query.get(self.author_id).name


class Book_Inventory(db.Model):
    __tablename__ = 'book_inventory'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    inventory_id = Column(Integer, ForeignKey(Inventory.id), nullable=False, default=1)
    quantity = Column(Integer, nullable=False)
    added_date = Column(DateTime, nullable=False, default=datetime.now())

    def __str__(self):
        return Inventory.query.get(self.inventory_id).name


class Account(db.Model, UserMixin):
    __tablename__ = 'account'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    avatar = Column(String(255), nullable=False,
                    default='avatar_male.png')
    email = Column(String(100), nullable=False, unique=True)
    register_date = Column(DateTime, default=datetime.now())
    last_login = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class User(Account):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birthday = Column(DateTime, nullable=False)
    phone = Column(String(12), nullable=False)
    gender = Column(Enum(GenderType), nullable=False, default=GenderType.MALE)
    address = Column(String(100), nullable=False)
    comments = relationship('Comment', backref='user', lazy=True)


class Admin(Account):
    __tablename__ = 'admin'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    role = Column(Enum(AdminRole), default=AdminRole.OWNER)


class Customer(User):
    __tablename__ = 'customer'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    customer_type = Column(Enum(CustomerType), nullable=False, default=CustomerType.GUEST)
    orders = relationship('Order', backref='customer', lazy=True)
    receipts = relationship('Receipt', backref='customer', lazy=True)


class Staff(User):
    __tablename__ = 'staff'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    job_title = Column(Enum(StaffJobTitle), nullable=False, default=StaffJobTitle.SALE)
    receipts = relationship('Receipt', backref='staff', lazy=True)


class Order(db.Model):
    __tablename__ = 'order'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_date = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    is_paid = Column(Boolean, nullable=False, default=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)


class OrderDetails(db.Model):
    __tablename__ = 'order_details'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Integer, nullable=False, default=10000)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)

    def __str__(self):
        return 'Order ' + str(Order.query.get(self.order_id).id)


class Receipt(db.Model):
    __tablename__ = 'receipt'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    staff_id = Column(Integer, ForeignKey(Staff.id))
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(db.Model):
    __tablename__ = 'receipt_details'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Integer, nullable=False, default=10000)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)

    def __str__(self):
        return 'Receipt ' + str(Receipt.query.get(self.receipt_id).id)


class Comment(db.Model):
    __tablename__ = 'comment'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(512), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)


class VNPAY_History(db.Model):
    __tablename__ = 'vnpay_history'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, nullable=False)
    bank_code = Column(String(20), nullable=False)
    description = Column(String(512), nullable=False)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()