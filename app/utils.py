import numpy
from app import dao
from flask_login import current_user


def count_cart(cart):
    total_amount, total_quantity = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        "total_amount": total_amount,
        "total_quantity": total_quantity
    }


def get_orders():
    orders = []
    for o in dao.get_orders(current_user.id):
        dao.update_order_status(o.id, o.status.name)
        details = dao.get_order_details(o.id)
        orders.append({
            'id': o.id,
            'created_date': o.created_date.strftime('%H:%M:%S %d/%m/%Y'),
            'status': o.status,
            'product_quantity': len(details),
            'total_price': numpy.sum([d.quantity * d.price for d in details]),
            'details': [{
                'quantity': d.quantity,
                'price': d.price,
                'book': dao.get_book_by_id(d.book_id)
            } for d in details]
        })

    return orders


def get_order_by_id(order_id):
    orders = []
    o = dao.get_order_by_id(order_id)
    dt = dao.get_order_details(order_id)
    orders.append({
        'id': order_id,
        'created_date': o.created_date.strftime('%H:%M:%S %d/%m/%Y'),
        'status': o.status,
        'is_paid': o.is_paid,
        'product_quantity': len(dao.get_order_details(o.id)),
        'total_price': numpy.sum([d.quantity * d.price for d in dt]),
        'sub_total': 0,
        'details': [{
            'quantity': d.quantity,
            'price': d.price,
            'book': dao.get_book_by_id(d.book_id)
        } for d in dt]
    })
    orders[0]['sub_total'] = numpy.sum([d['quantity'] * d['book'].price for d in orders[0]['details']])

    return orders[0]


def get_orders_summary(orders):
    summary = []
    sub_total = total = 0
    for o in orders:
        for d in o['details']:
            total += d['price'] * d['quantity']
            sub_total += d['book'].price * d['quantity']

    summary.append({
        'sub_total': sub_total,
        'total': total,
        'discount': total - sub_total,
        'tax': 11000
    })

    return summary[0]


def get_books(kw=None, cate_id=None):
    books = []
    for b in dao.get_books(desc=False, kw=kw, cate_id=cate_id):
        books.append({
            'id': b.id,
            'name': b.name,
            'image': b.image,
            'categories': [{
                'id': c.id,
                'name': c.__str__()
            } for c in b.categories],
            'authors': [{
                'id': a.id,
                'name': a.__str__()
            } for a in b.authors],
            'quantity': dao.get_book_inventory(b.id).quantity,
        })

    return books


def get_book(book_id):
    book = []
    b = dao.get_book_by_id(book_id)
    i = dao.get_inventory_by_id(dao.get_book_inventory(book_id).inventory_id)
    book.append({
        'id': b.id,
        'name': b.name,
        'price': b.price,
        'description': b.description,
        'published_date': b.published_date,
        'image': b.image,
        'categories': [{
            'id': int(c.id),
            'name': c.__str__()
        } for c in dao.get_categories_by_book_id(b.id)],
        'authors': [{
            'id': int(a.id),
            'name': a.__str__()
        } for a in dao.get_authors_by_book_id(b.id)],
        'inventory': {
            'id': int(i.id),
            'name': i.name
        },
        'quantity': dao.get_book_inventory(b.id).quantity,
    })

    return book[0]


def get_categories_string(book_id):
    string = ''
    for c in dao.get_categories_by_book_id(book_id):
        string += c.name + ', '

    return string
