from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose

admin = Admin(app=app, name='BookStore Manager', template_mode='bootstrap4')

class MyProductView(ModelView):
    pass


class MyCategoryView(ModelView):
    pass


class StatsView(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')



admin.add_view(StatsView(name='Thông kê báo cáo'))