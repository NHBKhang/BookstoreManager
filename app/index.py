import math
from flask import render_template, request, redirect
import dao
from app import app, login
from flask_login import login_user


@app.route('/')
def index():
    return render_template('admin/index.html')


@app.route("/admin/login", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        from app.models import Admin
        user = Admin.query.filter(username == username, password == password).first()
        if user:
            login_user(user=user)

    return redirect("/admin")


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
