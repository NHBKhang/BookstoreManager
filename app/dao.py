from app.models import Category, Book, Admin, User, Account, Book_Category, Book_Author, Author
from app import app
import hashlib


def get_categories():
    return Category.query.all()


def get_books(kw=None, cate_id=None, page=None):
    books = Book.query
    if kw:
        books = books.filter(Book.name.contains(kw))
    if cate_id:
        from app.models import Book_Category

        books = books.filter(Book.categories.any(Book_Category.category_id == cate_id))
    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size
        return books.slice(start, start + page_size)
    return books.all()


def count_books():  # Count number of product in database
    return Book.query.count()


def get_book_by_id(book_id):
    return Book.query.get(book_id)


def get_authors_by_book_id(book_id):
    book_author = Book_Author.query.filter(Book_Author.book_id == book_id).all()
    return [Author.query.get(a.author_id) for a in book_author]


def get_categories_by_book_id(book_id):
    book_category = Book_Category.query.filter(Book_Category.book_id == book_id).all()
    return [Category.query.get(a.category_id) for a in book_category]


def get_admin_by_id(admin_id):
    return Admin.query.get(admin_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)


def auth_admin(username, password):
    import hashlib

    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())  # Decrypt password from clients

    return Admin.query.filter(Admin.username.__eq__(username.strip()),
                              Admin.password.__eq__(password)).first()


if __name__ == '__main__':
    with app.app_context():
        pass