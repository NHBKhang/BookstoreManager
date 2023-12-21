import math
from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import logout_user, current_user, login_user, login_required
from flask_admin import expose
from app import dao, utils, app
from datetime import datetime


def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')
    page_size = app.config['PAGE_SIZE']

    books = dao.get_books(kw, cate_id, page)
    carousel_items = dao.get_carousel_items()

    num = dao.count_books()

    if kw or cate_id:
        num = len(books)
        return render_template('index.html', books=books, pages=math.ceil(num / page_size))
    if page:
        return render_template('index.html', books=books, pages=math.ceil(num / page_size))

    return render_template('index.html', books=books, amount=8, carousel_items=carousel_items,
                           index=True)


def cart():
    return render_template('cart.html')


def login():
    return render_template('login.html')


def logout():
    logout_user()
    return redirect(url_for('index'))


def register():
    return render_template('register.html')


def details(book_id):
    book = dao.get_book_by_id(book_id)
    authors = dao.get_authors_by_book_id(book_id)
    categories = dao.get_categories_by_book_id(book_id)
    comments = dao.get_comments(book_id)
    return render_template('details.html', book=book, authors=authors, b_categories=categories,
                           cate_len=len(categories), comments=comments)


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
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        gender = request.form.get("gender")
        birthday = request.form.get("birthday")
        phone = request.form.get("phone")
        address = request.form.get("address")
        email = request.form.get("email")

        from app.models import User
        if User.query.filter_by(username=username).first():
            err_msg = "Tên tài khoản đã tồn tại"
        elif password.strip() != conf_password.strip():
            err_msg = "Mật khẩu không khớp"
        else:
            from app.models import GenderType
            if gender == GenderType.FEMALE.__val__():
                avatar = 'avatar_female.png'
            else:
                avatar = 'avatar_male.png'

            try:
                dao.add_customer(username=username, password=password, first_name=first_name, last_name=last_name,
                             gender=gender, birthday=birthday, address=address, phone=phone, email=email, avatar=avatar)

                return redirect(url_for('login'))
            except:
                err_msg = "Hệ thống đang có lỗi! Vui lòng quay lại sau!"

    return render_template('register.html', err_msg=err_msg)


def add_to_cart():
    key = app.config['CART_KEY']
    cart = session.get(key)
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


def update_cart(book_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and book_id in cart:
        cart[book_id]['quantity'] = int(request.json['quantity'])

    session[key] = cart

    return jsonify(utils.count_cart(cart))


def delete_cart(book_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and book_id in cart:
        del cart[book_id]

    session[key] = cart

    return jsonify(utils.count_cart(cart))


@login_required
def pay():
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart:
        try:
            dao.save_receipt(cart=cart)
        except Exception as ex:
            print(str(ex))
            return jsonify({"status": 500})
        else:
            del session[key]

    return jsonify({"status": 200})