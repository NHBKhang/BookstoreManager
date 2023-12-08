import dao, utils
from flask import session
from app import app, dao, login


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
    from app import admin, urls

    app.run(debug=True)
