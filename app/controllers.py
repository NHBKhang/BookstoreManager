import math
from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import logout_user, current_user, login_user
from flask_admin import expose
from app import dao, utils, app


def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    amount = 8

    books = dao.get_books(kw, cate_id, amount=amount)
    recommend_books = dao.get_recommend_book()

    if kw != None or cate_id != None:
        num = len(books)
        page_size = app.config['PAGE_SIZE']
        return render_template('list.html', books=books, pages=math.ceil(num / page_size))

    return render_template('index.html', books=books, amount=amount, recommend_books=recommend_books)


def list():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')

    books = dao.get_books(kw, cate_id, page)

    num = dao.count_books()
    page_size = app.config['PAGE_SIZE']

    return render_template('list.html', books=books, pages=math.ceil(num / page_size))


def cart():
    return render_template('cart.html')


def login():
    return render_template('login.html')


def logout():
    logout_user()
    return redirect(url_for("index"))


def register():
    return render_template('register.html')


def details(book_id):
    book = dao.get_book_by_id(book_id)
    authors = dao.get_authors_by_book_id(book_id)
    categories = dao.get_categories_by_book_id(book_id)
    # comments = dao.load_comments(book_id)
    return render_template('details.html', book=book, authors=authors, b_categories=categories,
                           cate_len=len(categories))


def sales():
    return render_template('sales/index.html')


def admin_login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = dao.auth_account(username=username, password=password, type='admin')
        if user:
            login_user(user=user)
        else:
            return render_template('/admin/login.html', err_acc=True)

    return redirect('/admin')


@expose("/")
def admin_logout():
    logout_user()
    return redirect('/admin')


def user_login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = dao.auth_account(username=username, password=password)
        if user:
            login_user(user=user)
        else:
            return render_template('login.html', err_acc=True)

    return redirect(url_for('index'))


def user_register():
    err_msg = ''
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        conf_password = request.form.get("confirm-password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        gender = request.form.get("gender")
        birthday = request.form.get("birthday")
        phone = request.form.get("phone")
        address = request.form.get("address")
        email = request.form.get("email")

        from app.models import User
        if User.query.filter(User.username.__eq__(username.strip())):
            err_msg = "Tên tài khoản đã tồn tại"
        elif password.strip() != conf_password.strip():
            err_msg = "Mật khẩu không khớp"
        else:
            err_msg = ""
            dao.add_user(username=username, password=password, first_name=first_name, last_name=last_name,
                         gender=gender, birthday=birthday, address=address, phone=phone, email=email)

    return render_template('register.html', err_msg=err_msg)


def add_to_cart():
    cart = session.get('cart')
    if cart is None:
        cart = {}

    data = request.json
    id = str(data.get("id"))

    if id in cart:  # sp da co trong gio
        cart[id]['quantity'] += 1
    else:  # san pham chua co trong gio
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))
