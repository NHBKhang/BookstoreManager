from app.models import Category, Book, Admin, User
from app import app
import hashlib


def get_categories():
    return Category.query.all()


def get_books(kw=None, cate_id=None, page=None):
    books = Book.query
    if kw:
        books = books.filter(Book.name.contains(kw))
    if cate_id:
        books = books.filter(Book.category_id.__eq__(cate_id))
    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size
        return books.slice(start, start + page_size)
    return books.all()


def count_books():  # Count number of product in database
    return Book.query.count()


def get_admin_by_id(admin_id):
    return Admin.query.get(admin_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)


def auth_admin(username, password):
    import hashlib

    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()) #Decrypt password from clients

    return Admin.query.filter(Admin.username.__eq__(username.strip()),
                             Admin.password.__eq__(password)).first()