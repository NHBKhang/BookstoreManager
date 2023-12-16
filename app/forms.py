from wtforms import Form, StringField, BooleanField, IntegerField, TextAreaField, DateField, FieldList, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, Email
from app import dao, app


class AuthorForm(Form):
    name = StringField('Tên tác giả', validators=[DataRequired(), Length(min=1, max=50)])


class BookForm(Form):
    name = StringField('Tên sách', validators=[DataRequired(), Length(min=1, max=50)])
    price = IntegerField('Giá', validators=[DataRequired(), NumberRange(min=1000, max=1000000)])
    active = BooleanField('Có sẵn?', validators=[DataRequired()], default=True)
    description = TextAreaField('Miêu tả', validators=[DataRequired()])
    image = StringField('Ảnh')
    published_date = DateField('Ngày phát hành', validators=[DataRequired()])
    with app.app_context():
        authors = FieldList(SelectField(label='', choices=[x for x in dao.get_authors()]), validators=[DataRequired()],
                            min_entries=1, max_entries=3, label='Tác giả')
        categories = FieldList(SelectField(label='', choices=[x for x in dao.get_categories()]),
                               validators=[DataRequired()], min_entries=1, max_entries=10, label='Thể loại')
        inventories = FieldList(SelectField(label='', choices=[x for x in dao.get_inventories()]),
                               validators=[DataRequired()], min_entries=1, max_entries=50, label='Kho')


class CategoryForm(Form):
    name = StringField('Tên thể loại', validators=[DataRequired(), Length(min=1, max=50)])


class InventoryForm(Form):
    name = StringField('Tên kho', validators=[DataRequired(), Length(min=1, max=50)])