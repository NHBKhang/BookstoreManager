from app import db
from app.views import *
from app.models import Category, Book, User, Inventory, Author
from flask_admin import Admin


@app.route('/admin/delete_book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    dao.delete_book_by_id(book_id)


admin = Admin(app=app, name='Quản Lí Nhà Sách', template_mode='bootstrap4',
              index_view=MyAdminIndexView(name='Trang chủ', menu_icon_type="fa", menu_icon_value="fa-home"))

admin.add_view(MyUserView(User, db.session, name='Người dùng', menu_icon_type="fa", menu_icon_value="fa-users"))
admin.add_view(MyBookView(Book, db.session, name='Sách', menu_icon_type="fa", menu_icon_value="fa-book"))
admin.add_view(MyCategoryView(Category, db.session, name='Thể loại', menu_icon_type="fa", menu_icon_value="fa-list"))
admin.add_view(MyAuthorView(Author, db.session, name='Tác giả', menu_icon_type="fa", menu_icon_value="fa-user"))
admin.add_view(MyInventoryView(Inventory, db.session, name='Kho', menu_icon_type="fa", menu_icon_value="fa-box"))
admin.add_view(MyStatsView(name='Thống kê báo cáo', menu_icon_type="fa", menu_icon_value="fa-calculator"))
admin.add_view(MyRevenueStatsView(name='Thống kê báo cáo doanh thu', url='/admin/revenue_stats'))
admin.add_view(MyFrequencyStatsView(name='Thống kê báo cáo tần suất', url='/admin/frequency_stats'))
admin.add_category(name='Tiện ích khác', icon_type="fa", icon_value="fa-bars")
admin.add_view(ManageBooksView(name='Quản lý sách', endpoint='manage_books', category='Tiện ích khác',
                               menu_icon_type="fa", menu_icon_value="fa-book-medical"))
admin.add_view(EditRulesView(name='Đổi quy định', endpoint='edit_rules', category='Tiện ích khác', menu_icon_type="fa",
                             menu_icon_value="fa-ruler"))
admin.add_view(AddBookView('Thêm sách', url='/admin/add_books'))
admin.add_view(UpdateBookView('Cập nhật sách', url='/admin/update_books/<int:book_id>'))
