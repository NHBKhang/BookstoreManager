import numpy
from flask import request, redirect, jsonify
from flask_admin import BaseView, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app import dao, utils
from app.forms import *
from datetime import datetime


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        from app import models
        return current_user.is_authenticated and type(current_user) == models.Admin


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.categories_stats()
        return self.render('admin/index.html', stats=stats)


class MyBookView(ModelView):
    column_list = ['name', 'price', 'active']
    column_searchable_list = ['name']
    column_filters = ['price', 'name', 'active']
    edit_modal = True
    create_modal = True
    can_export = True
    can_view_details = True
    form = BookForm


class MyCategoryView(ModelView):
    column_list = ['name']
    column_searchable_list = ['name']
    edit_modal = True
    create_modal = True
    form = CategoryForm


class MyAuthorView(ModelView):
    column_list = ['name']
    edit_modal = True
    create_modal = True
    form = AuthorForm


class MyUserView(ModelView):
    column_list = ['username', 'first_name', 'last_name', 'email', 'phone']
    column_searchable_list = ['username']
    can_create = False
    can_view_details = True
    form = UserForm


class MyInventoryView(ModelView):
    column_list = ['name']
    column_editable_list = ['name']
    column_searchable_list = ['name']
    edit_modal = True
    create_modal = True
    form = InventoryForm


class MyStatsView(BaseView):
    @expose("/")
    def index(self):
        stats = dao.books_revenue_stats(kw=request.args.get('kw'),
                                        from_date=request.args.get('from_date'),
                                        to_date=request.args.get('to_date'))

        return self.render('admin/stats/stats.html', stats=stats)


class MyRevenueStatsView(BaseView):
    @expose("/")
    def index(self):
        month = request.args.get('month')
        num = []
        if month:
            num = month.split('-')
        try:
            num[1]
        except IndexError:
            num.append(datetime.now().year)
            num.append(datetime.now().month)

        stats = dao.categories_revenue_stats(num[1], num[0])
        total = dao.categories_total_revenue(num[1], num[0])

        return self.render('admin/stats/revenue-stats.html', stats=stats, total=total,
                           month=str(num[1]) + '/' + str(num[0]))

    def is_visible(self):
        return False


class MyFrequencyStatsView(BaseView):
    @expose("/")
    def index(self):
        month = request.args.get('month')
        num = []
        if month:
            num = month.split('-')
        try:
            num[1]
        except IndexError:
            num.append(datetime.now().year)
            num.append(datetime.now().month)

        stats = dao.books_frequency_stats(num[1], num[0])

        return self.render('admin/stats/frequency-stats.html', stats=stats, total=numpy.sum([s[1] for s in stats]),
                           month=str(num[1]) + '/' + str(num[0]))

    def is_visible(self):
        return False


class ManageBooksView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def manage_books(self):
        kw = request.args.get('keyword')
        cate_id = request.args.get('categories')

        books = utils.get_books(kw=kw, cate_id=cate_id)
        return self.render('admin/books/manage-books.html', books=books)


class EditRulesView(BaseView):
    @expose('/')
    def edit_rules(self):
        return self.render('admin/edit-rules.html')


class AddBookView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def add_book(self):
        a = dao.get_authors()
        i = dao.get_inventories()

        if request.method == "POST":
            name = request.form.get('name')
            description = request.form.get('description')
            price = request.form.get('price')
            image = request.form.get('image')
            published_date = request.form.get('published-date')
            categories = request.form.get('categories')
            authors = request.form.get('authors')
            inventory = request.form.get('inventory')
            quantity = request.form.get('quantity')

            try:
                b = dao.add_book(name=name, description=description, price=int(price), img=image, date=published_date)
                for c in categories:
                    dao.add_book_category(b.id, int(c))
                for a in authors:
                    dao.add_book_author(b.id, int(a))
                dao.add_book_inventory(b.id, int(inventory), int(quantity))
                if request.form.get('back'):
                    return redirect('/admin/manage_books')
            except Exception as ex:
                print(str(ex))
                return jsonify({"status": 500})

        return self.render('admin/books/add-books.html', authors=a, inventories=i)

    def is_visible(self):
        return False


class UpdateBookView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def update_book(self, book_id):
        if dao.get_book_by_id(book_id) is None:
            return redirect('/admin/manage_books')

        a = dao.get_authors()
        i = dao.get_inventories()
        book = utils.get_book(book_id)

        if request.method == "POST":
            name = request.form.get('name')
            description = request.form.get('description')
            price = request.form.get('price')
            image = request.form.get('image')
            published_date = request.form.get('published-date')
            categories = request.form.get('categories')
            authors = request.form.get('authors')
            inventory = request.form.get('inventory')
            quantity = request.form.get('quantity')

            try:
                dao.update_book(book_id=book_id, name=name, description=description, price=price, image=image,
                                published_date=published_date)
                for c in categories:
                    dao.add_book_category(book_id, int(c))
                for a in authors:
                    dao.add_book_author(book_id, int(a))
                dao.add_book_inventory(book_id, int(inventory), int(quantity))
                if request.form.get('back'):
                    return redirect('/admin/manage_books')
                else:
                    s = '/admin/update_books/' + str(book_id + 1)
                    return redirect(s)
            except Exception as ex:
                print(str(ex))
                return jsonify({"status": 500})

        return self.render('admin/books/update-books.html', authors=a, inventories=i, book=book)

    def is_visible(self):
        return False
