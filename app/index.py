from flask import session
from app import dao, login, utils, app
from datetime import datetime


@app.context_processor
def common_resp():
    return {
        'categories': dao.get_categories(),
        'cart': utils.count_cart(session.get(app.config['CART_KEY'])),
        'today': datetime.now().strftime('%Y-%m-%d'),
        'date': datetime.now().strftime('%d/%m/%Y'),
        'rule': dao.get_rule()
    }


@login.user_loader
def get_account(user_id):
    user = dao.get_user_by_id(user_id)

    return user


if __name__ == '__main__':
    from app import urls, admin

    app.run(debug=True)
