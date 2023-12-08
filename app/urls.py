import math
from flask import render_template, request, redirect, session, jsonify
from flask_login import login_user, logout_user, current_user
from app import app, dao, utils


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    if current_user:
       logout_user()
    return redirect('/')


@app.route('/')
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')

    books = dao.get_books(kw, cate_id, page)

    num = dao.count_books()
    page_size = app.config['PAGE_SIZE']

    return render_template('index.html', books=books, pages=math.ceil(num / page_size))


@app.route("/books/<int:book_id>")
def details(book_id):
    book = dao.get_book_by_id(book_id)
    authors = dao.get_authors_by_book_id(book_id)
    categories = dao.get_categories_by_book_id(book_id)
    # comments = dao.load_comments(book_id)
    return render_template('details.html', book=book, authors=authors, b_categories=categories,
                           cate_len=len(categories))


@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username != '' and password != '':
            user = dao.auth_account(username=username, password=password, type='admin')
            if user:
                login_user(user=user)
            else:
                return render_template('/admin/login.html', err_acc=True)

    return redirect('/admin')


@app.route('/login', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username != '' and password != '':
            user = dao.auth_account(username=username, password=password)
            if user:
                login_user(user=user)
            else:
                return render_template('login.html', err_acc=True)

        return redirect('/')


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
