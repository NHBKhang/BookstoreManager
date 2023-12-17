from flask import session
from app import dao, login, utils, app
from datetime import datetime


@app.context_processor
def common_resp():
    return {
        'categories': dao.get_categories(),
        'cart': utils.count_cart(session.get('cart')),
        'today': datetime.now().strftime('%Y-%m-%d')
    }


@login.user_loader
def get_account(account_id):
    user = dao.get_admin_by_id(account_id)
    if user is None:
        user = dao.get_user_by_id(account_id)

    return user


if __name__ == '__main__':
    from app import urls, admin

    app.run(debug=True)
