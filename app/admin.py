from app import db
from app.forms import *
from app.models import Category, Book, User, Inventory, Author
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect, request

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
    edit_modal = True
    can_create = False
    can_view_details = True


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


class AddBooksView(BaseView):
    @expose('/')
    def add_books(self):
        authors = dao.get_authors()
        books = dao.get_books()
        return self.render('admin/add-books.html', books=books, authors=authors)


class EditRulesView(BaseView):
    @expose('/')
    def edit_rules(self):
        return self.render('admin/edit-rules.html')


admin.add_view(MyUserView(User, db.session, name='Người dùng', menu_icon_type="fa", menu_icon_value="fa-users"))
admin.add_view(MyBookView(Book, db.session, name='Sách', menu_icon_type="fa", menu_icon_value="fa-book"))
admin.add_view(MyCategoryView(Category, db.session, name='Thể loại', menu_icon_type="fa", menu_icon_value="fa-list"))
admin.add_view(MyAuthorView(Author, db.session, name='Tác giả', menu_icon_type="fa", menu_icon_value="fa-user"))
admin.add_view(MyInventoryView(Inventory, db.session, name='Kho', menu_icon_type="fa", menu_icon_value="fa-box"))
admin.add_view(MyStatsView(name='Thống kê báo cáo', menu_icon_type="fa", menu_icon_value="fa-calculator"))
admin.add_category(name='Tiện ích khác', icon_type="fa", icon_value="fa-bars")
admin.add_view(AddBooksView(name='Nhập sách', endpoint='add_books', category='Tiện ích khác', menu_icon_type="fa",
                           menu_icon_value="fa-book-medical"))
admin.add_view(EditRulesView(name='Đổi quy định', endpoint='edit_rules', category='Tiện ích khác', menu_icon_type="fa",
                           menu_icon_value="fa-book-medical"))
