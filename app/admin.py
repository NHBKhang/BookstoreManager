from app import db, app, utils
from app.forms import *
from app.models import Category, Book, User, Inventory, Author
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect, request, jsonify

admin = Admin(app=app, name='Quản Lí Nhà Sách', template_mode='bootstrap4',
              index_view=AdminIndexView(name='Trang chủ', menu_icon_type="fa", menu_icon_value="fa-home"))


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        from app import models
        return current_user.is_authenticated and type(current_user) == models.Admin


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


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
        # stats = dao.stats_revenue(kw=request.args.get('kw'),
        #                           from_date=request.args.get('from_date'),
        #                           to_date=request.args.get('to_date'))
        stats = []
        return self.render('admin/stats.html', stats=stats)


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


@app.route('/admin/delete_book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    dao.delete_book_by_id(book_id)


admin.add_view(MyUserView(User, db.session, name='Người dùng', menu_icon_type="fa", menu_icon_value="fa-users"))
admin.add_view(MyBookView(Book, db.session, name='Sách', menu_icon_type="fa", menu_icon_value="fa-book"))
admin.add_view(MyCategoryView(Category, db.session, name='Thể loại', menu_icon_type="fa", menu_icon_value="fa-list"))
admin.add_view(MyAuthorView(Author, db.session, name='Tác giả', menu_icon_type="fa", menu_icon_value="fa-user"))
admin.add_view(MyInventoryView(Inventory, db.session, name='Kho', menu_icon_type="fa", menu_icon_value="fa-box"))
admin.add_view(MyStatsView(name='Thống kê báo cáo', menu_icon_type="fa", menu_icon_value="fa-calculator"))
admin.add_category(name='Tiện ích khác', icon_type="fa", icon_value="fa-bars")
admin.add_view(
    ManageBooksView(name='Quản lý sách', endpoint='manage_books', category='Tiện ích khác', menu_icon_type="fa",
                    menu_icon_value="fa-book-medical"))
admin.add_view(EditRulesView(name='Đổi quy định', endpoint='edit_rules', category='Tiện ích khác', menu_icon_type="fa",
                             menu_icon_value="fa-ruler"))
admin.add_view(AddBookView('Thêm sách', url='/admin/add_books'))
admin.add_view(UpdateBookView('Cập nhật sách', url='/admin/update_books/<int:book_id>'))
