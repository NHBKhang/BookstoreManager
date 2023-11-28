import math, dao, utils
from flask import render_template, request, redirect, session, jsonify
from app import app, login
from flask_login import login_user, logout_user, current_user


@app.route('/')
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')

    books = dao.get_books(kw, cate_id, page)

    num = dao.count_books()
    page_size = app.config['PAGE_SIZE']

    return render_template('index.html', books=books, pages=math.ceil(num / page_size))


@app.route("/admin/login", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username != '' and password != '':
            user = dao.auth_admin(username=username, password=password)
            if user:
                login_user(user=user)
        else:
            if username == '':
                err_usr_dis = 'block'
            else:
                err_usr_dis = 'none'
            if password == '':
                err_pwd_dis = 'block'
            else:
                err_pwd_dis = 'none'
            return render_template('admin/login.html', err_usr_dis=err_usr_dis, err_pwd_dis=err_pwd_dis)

    return redirect("/admin")


# @app.route("/layout/header", methods=['GET', 'POST'])
# def login_admin():
#     if request.method == 'POST':
#         username = request.form.get("username")
#         password = request.form.get("password")
#
#         if username != '' and password != '':
#             user = dao.auth_admin(username=username, password=password)
#             if user:
#                 login_user(user=user)
#         else:
#             if username == '':
#                 err_usr_dis = 'block'
#             else:
#                 err_usr_dis = 'none'
#             if password == '':
#                 err_pwd_dis = 'block'
#             else:
#                 err_pwd_dis = 'none'
#             return render_template('layout/index.html', err_usr_dis=err_usr_dis, err_pwd_dis=err_pwd_dis)
#
#     return redirect("/")


@app.route("/books/<int:book_id>")
def details(book_id):
    book = dao.get_book_by_id(book_id)
    authors = dao.get_authors_by_book_id(book_id)
    categories = dao.get_categories_by_book_id(book_id)
    # comments = dao.load_comments(book_id)
    return render_template('details.html', book=book, authors=authors, categories=categories, cate_len=len(categories))


@app.route('/api/cart', methods=['post'])
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


@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.context_processor
def common_resp():
    return {
        'categories': dao.get_categories(),
        'cart': utils.count_cart(session.get('cart'))
    }


@login.user_loader
def get_account(account_id):
    user = dao.get_admin_by_id(account_id)
    if user is None:
        user = dao.get_user_by_id(account_id)

    return user


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
