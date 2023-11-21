from flask import render_template

from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('*******', methods=['post'])
def login_admin():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user)

    return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)
