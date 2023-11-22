import math
from flask import render_template, request, redirect
import dao
from app import app, login
from flask_login import login_user


@app.route('/')
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')

    cates = dao.get_categories()
    books = dao.get_books(kw, cate_id, page)

    num = dao.count_books()
    page_size = app.config['PAGE_SIZE']

    return render_template('index.html', categories=cates, books=books, pages=math.ceil(num / page_size))


@app.route("/admin/login", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if username != '' and password != '':
            user = dao.auth_admin(username=username, password=password)
            if user:
                login_user(user=user)

    return redirect("/admin")


@login.user_loader
def get_admin(admin_id):
    return dao.get_admin_by_id(admin_id)


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
