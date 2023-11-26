from app import app, db
from app.forms import BookViewForm
from app.models import Category, Book, User, Inventory
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect

admin = Admin(app=app, name='BookStore Manager', template_mode='bootstrap4')


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        from app import models
        return current_user.is_authenticated and type(current_user) == models.Admin


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyBookView(ModelView):
    column_list = ['name', 'price']
    column_searchable_list = ['name']
    column_filters = ['price', 'name']
    column_editable_list = ['name', 'price']
    edit_modal = True
    create_modal = True
    can_export = True
    form = BookViewForm


class MyCategoryView(ModelView):
    column_list = ['name', 'products']
    column_searchable_list = ['name']
    edit_modal = True
    create_modal = True


class MyUserView(ModelView):
    column_list = ['username', 'first_name', 'last_name']
    edit_modal = True
    create_modal = True


class MyInventoryView(ModelView):
    column_list = ['name']
    column_editable_list = ['name']
    column_searchable_list = ['name']
    edit_modal = True
    create_modal = True



class MyStatsView(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')


@app.route('/admin/logout')
@expose("/")
def logout_admin():
    logout_user()
    return redirect('/admin')


admin.add_view(MyUserView(User, db.session, menu_icon_type="fa", menu_icon_value="fa-users"))
admin.add_view(MyCategoryView(Category, db.session, menu_icon_type="fa", menu_icon_value="fa-list"))
admin.add_view(MyBookView(Book, db.session, menu_icon_type="fa", menu_icon_value="fa-book"))
admin.add_view(MyInventoryView(Inventory, db.session, menu_icon_type="fa", menu_icon_value="fa-box"))
admin.add_view(MyStatsView(name='Thống kê báo cáo', menu_icon_type="fa", menu_icon_value="fa-calculator"))
