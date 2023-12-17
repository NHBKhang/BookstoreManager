from app.models import *
from app import db, app
from sqlalchemy import desc
import hashlib, json, os


def get_categories():
    return Category.query.all()


def get_books(kw=None, cate_id=None, page=None, desc=True, amount=None):
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
        books = books.slice(start, start + page_size)
    if desc:
        books = books.order_by(Book.id.desc())
    if amount:
        books = books.limit(amount)

    return books.all()


def get_recommend_book():
    with open(os.path.join(app.root_path, "static/data/carousel.json"), encoding="utf-8") as rb:
        return json.load(rb)


def get_authors():
    return Author.query.all()


def get_inventories():
    return Inventory.query.all()


def count_books():  # Count number of product in database
    return Book.query.count()


def get_book_by_id(book_id):
    return Book.query.get(book_id)


def get_book_by_name(book_name):
    return Book.query.get(book_name).first()


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


def auth_account(username, password, type='user'):
    import hashlib

    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    if type == 'user':
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()
    else:
        return Admin.query.filter(Admin.username.__eq__(username.strip()),
                                  Admin.password.__eq__(password)).first()


def add_admin(username, password, name, email, status=AccountStatus.ACTIVE, avatar='avatar_male.png'):
    admin = Admin(username=username, password=hashlib.md5(password.strip().encode('utf-8')).hexdigest(), status=status,
                  avatar=avatar, name=name, email=email)
    db.session.add(admin)
    db.session.commit()


def add_user(username, password, first_name, last_name, birthday, email, phone, address, gender=GenderType.MALE,
             status=AccountStatus.ACTIVE, avatar='avatar_male.png'):
    import hashlib
    user = User(username=username, password=hashlib.md5(password.strip().encode('utf-8')).hexdigest(), status=status,
                avatar=avatar, first_name=first_name, last_name=last_name,
                birthday=datetime.strptime(birthday, '%Y-%m-%d'), phone=phone, email=email,
                gender=gender, address=address)
    db.session.add(user)
    db.session.commit()
    return user


def add_customer(username, password, first_name, last_name, birthday, email, phone, address, gender=GenderType.MALE,
                 status=AccountStatus.ACTIVE, avatar='avatar_male.png', customer_type=CustomerType.GUEST):
    customer = Customer(username=username, password=hashlib.md5(password.strip().encode('utf-8')).hexdigest(),
                        status=status, avatar=avatar, first_name=first_name, last_name=last_name, phone=phone,
                        birthday=datetime.strptime(birthday, '%Y-%m-%d'), email=email, gender=gender,
                        address=address, customer_type=customer_type)
    db.session.add(customer)
    db.session.commit()


def add_staff(user_id, job_title=StaffJobTitle.SALE):
    customer = Customer(user_id=user_id, job_title=job_title)
    db.session.add(customer)
    db.session.commit()


def add_book(name, price, img, description, date):
    b1 = Book(name=name, price=price,
              image=img,
              description=description,
              published_date=datetime.strptime(date, '%d/%m/%Y'))
    db.session.add_all([b1])
    db.session.commit()


def add_book_inventory(book_id, inventory_id=1, quantity=100):
    bi = Book_Inventory(book_id=book_id, inventory_id=inventory_id, quantity=quantity)
    db.session.add(bi)
    db.session.commit()


def add_book_category(book_id, category_id):
    ba = Book_Author(book_id=book_id, author_id=category_id)
    db.session.add(ba)
    db.session.commit()


def add_book_author(book_id, author_id):
    ba = Book_Author(book_id=book_id, author_id=author_id)
    db.session.add(ba)
    db.session.commit()
