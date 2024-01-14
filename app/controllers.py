import math
from flask import render_template, request, redirect, url_for, session, jsonify, flash
from flask_login import logout_user, current_user, login_user, login_required
from flask_admin import expose
from app import dao, utils, app, otp
from datetime import datetime


def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')
    page_size = app.config['PAGE_SIZE']

    books = dao.get_books(kw, cate_id, page)
    carousel_items = dao.get_carousel_items()

    num = dao.count_books()

    if kw or cate_id or page:
        if kw or cate_id:
            num = len(books)
        return render_template('index.html', books=books, pages=math.ceil(num / page_size),
                               page=page if page else "", cate_id=cate_id if cate_id else "", kw=kw if kw else "")

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
                           comments=comments)


@login_required
def my_orders():
    orders = utils.get_orders()
    summary = utils.get_orders_summary(orders)

    return render_template('my-orders.html', orders=orders, summary=summary)


@login_required
def my_order_details(order_id):
    order = utils.get_order_by_id(order_id)
    user = dao.get_user_by_id(current_user.id)

    return render_template('my-orders-details.html', order=order, user=user)


def staff_login():
    books = dao.get_books(kw=request.args.get('kw'))
    customers = dao.get_customers()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_account(username, password, 'staff')
        try:
            from app.models import Staff
            staff = Staff.query.get(user.id)
        except Exception as e:
            print(e)
        if user:
            login_user(user)
            return render_template('/sales/index.html', books=books, customers=customers,
                                   user=dao.get_user_by_id(user.id))
        else:
            return render_template('/sales/index.html', books=books, err_msg=True)

    user = dao.get_user_by_id(current_user.id)
    return render_template('/sales/index.html', books=books, customers=customers,
                           user=user if user else dao.get_admin_by_id(current_user.id))


def sales():
    books = dao.get_books(kw=request.args.get('kw'))
    if current_user:
        redirect('/sales/login')

    return render_template('sales/index.html', books=books)


def staff_logout():
    logout_user()
    return redirect('/sales')


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

        user = dao.auth_account(username=username, password=password, type='user')
        if user:
            login_user(user=user)

            return redirect(url_for(request.args.get('next', 'index')))
        else:
            return render_template('login.html', err_acc=True)

    return render_template('login.html')


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
                dao.add_customer(username=username, password=password, name=username, first_name=first_name, last_name=last_name,
                                 gender=gender, birthday=birthday, address=address, phone=phone, email=email,
                                 avatar=avatar)

                return redirect(url_for('login'))
            except:
                err_msg = "Hệ thống đang lỗi! Vui lòng quay lại sau!"

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
            "quantity": 1,
            "max_quantity": dao.get_book_inventory(id).quantity
        }

    session[key] = cart

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


def add_to_sales_cart():
    key = app.config['SALES_KEY']
    cart = session.get(key)
    if cart is None:
        cart = {}

    data = request.json
    id = str(data.get("id"))
    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1,
            "max_quantity": dao.get_book_inventory(id).quantity
        }
    session[key] = cart

    return jsonify(utils.count_sales_cart(cart))


def update_sales_cart(book_id):
    key = app.config['SALES_KEY']
    cart = session.get(key)

    if request.method == "PUT":
        if cart and book_id in cart:
            cart[book_id]['quantity'] = int(request.json['quantity'])
    else:
        if cart and book_id in cart:
            del cart[book_id]

    session[key] = cart

    return jsonify(utils.count_sales_cart(cart))


@login_required
def payment():
    return render_template('payment.html')


@login_required
def pay():
    key = app.config['CART_KEY']
    cart = session.get(key)
    method = request.form.get('payment')
    order = None
    otp_valid = otp.verify_otp(current_user.email, request.form.get('otp'))

    if cart:
        try:
            method = int(method)
            if method == 3:
                order = dao.save_order(cart=cart, is_paid=True)
            elif method == 4:
                if otp_valid is True:
                    order = dao.save_order(cart=cart)
                    utils.send_payment_message(order, order.is_paid)
        except Exception as ex:
            print(str(ex))
            return jsonify({"status": 500})
        else:
            del session[key]

    if method == 3:
        return redirect(utils.pay_with_vnpay(request, order))
    else:
        if otp_valid is True:
            return redirect('/my_orders/' + str(order.id))
        else:
            return redirect('/payment')


@login_required
def pay_invoice():
    key = app.config['SALES_KEY']
    cart = session.get(key)
    customer_id = request.form.get('customer')

    try:
        receipt = dao.save_receipt(cart, customer_id=customer_id, staff_id=current_user.id)
    except Exception as e:
        print(e)
        return jsonify({"status": 500})

    return render_template('sales/invoice.html', receipt=receipt,
                           customer=dao.get_user_by_id(customer_id), staff=dao.get_user_by_id(current_user.id))


def export_invoice():
    key = app.config['SALES_KEY']
    cart = session.get(key)
    customer_id = request.args.get('customer')
    try:
        receipt = dao.save_receipt(cart, customer_id=customer_id, staff_id=current_user.id)
    except Exception as e:
        print(e)
        return jsonify({"status": 500})

    return render_template('/sales/export-invoice.html', customer=dao.get_user_by_id(customer_id),
                           staff=dao.get_user_by_id(current_user.id), receipt=receipt)


@login_required
def invoice_return():
    key = app.config['SALES_KEY']

    del session[key]

    return redirect('/sales/login')


def comments(book_id):
    data = []
    for c in dao.get_comments(book_id=book_id):
        data.append({
            'id': c.id,
            'content': c.content,
            'created_date': str(c.created_date),
            'user': {
                'name': c.user.username,
                'avatar': c.user.avatar
            }
        })

    return jsonify(data)


def add_comment(book_id):
    content = request.json['content']
    if content == '':
        return jsonify({'status': 501})

    try:
        c = dao.save_comment(book_id=book_id, content=content)
    except Exception as e:
        print(e)
        return jsonify({'status': 500})

    return jsonify({
        'status': 204,
        'comment': {
            'id': c.id,
            'content': c.content,
            'created_date': str(c.created_date),
            'user': {
                'name': c.user.username,
                'avatar': c.user.avatar
            }
        }
    })


def edit_rules():
    min_quantity = request.form.get('min-quantity')
    max_quantity = request.form.get('max-quantity')
    expired_hours = request.form.get('expired-hours')
    print(min_quantity, max_quantity, expired_hours)

    dao.edit_rule(int(min_quantity), int(max_quantity), int(expired_hours))
    return redirect('/admin/edit_rules/')


def vnpay_return():
    vnp_TransactionNo = request.args.get('vnp_TransactionNo')
    vnp_TxnRef = request.args.get('vnp_TxnRef')
    vnp_Amount = request.args.get('vnp_Amount')
    vnp_ResponseCode = request.args.get('vnp_ResponseCode')
    vnp_BankCode = request.args.get('vnp_BankCode')
    order_id = int(vnp_TxnRef.split('-')[0])

    utils.send_payment_message(dao.get_order_by_id(order_id), True)
    v = dao.save_vnpay_history(vnp_TransactionNo, vnp_BankCode, request.args.get('vnp_OrderInfo'))
    dao.update_order(order_id, v.id)

    if vnp_ResponseCode == '00':
        try:
            flash('Cập nhật trạng thái thanh toán thành công.')
        except Exception as e:
            print(f"Error updating database: {str(e)}")
            flash('Lỗi cập nhật trạng thái thanh toán.')

    else:
        flash('Lỗi thanh toán. Vui lòng thử lại hoặc liên hệ với hỗ trợ.')

    return render_template('vnpay-return.html', transaction_no=vnp_TransactionNo, txn_ref=vnp_TxnRef,
                           amount=int(vnp_Amount), response_code=vnp_ResponseCode, bank_code=vnp_BankCode,
                           order_id=order_id)


@login_required
def send_otp():
    if request.method == 'SEND':
        otp.send_otp(current_user.email)

    return jsonify({'status': 'sent'})
