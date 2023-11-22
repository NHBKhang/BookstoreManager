from app.models import Category, Product, Admin
from app import app
import hashlib


def get_category():
    return Category.query.all()


def get_product(kw=None, cate_id=None, page=None):
    products = Product.query
    if kw:
        products = products.filter(Product.name.contains(kw))
    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))
    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size
        return products.slice(start, start + page_size)
    return products.all()


def count_product():  # Count number of product in database
    return Product.query.count()


def get_admin_by_id(admin_id):
    return Admin.query.get(admin_id)


def auth_admin(username, password):
    import hashlib

    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()) #Decrypt password from clients

    return Admin.query.filter(Admin.username.__eq__(username.strip()),
                             Admin.password.__eq__(password)).first()