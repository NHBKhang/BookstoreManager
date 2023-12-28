from wtforms import widgets, Form, StringField, BooleanField, IntegerField, TextAreaField, DateField, PasswordField, \
    SelectMultipleField, SelectField, HiddenField
from wtforms.validators import DataRequired, NumberRange, Length, Email
from app import dao, app


class UserForm(Form):
    from app.models import GenderType
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    active = BooleanField('Active?')
    last_name = StringField('Last name', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    birthday = DateField('Birthday', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[GenderType.MALE, GenderType.FEMALE])
    address = StringField('Address', validators=[DataRequired()])


class AuthorForm(Form):
    name = StringField('Author Name', validators=[DataRequired(), Length(min=1, max=50)])


class BookForm(Form):
    name = StringField('Tên sách', validators=[DataRequired(), Length(min=1, max=50)])
    price = IntegerField('Giá', validators=[DataRequired(), NumberRange(min=1000, max=1000000)])
    active = BooleanField('Có sẵn?', validators=[DataRequired()], default=True)
    description = TextAreaField('Miêu tả', validators=[DataRequired()])
    image = StringField('Ảnh')
    published_date = DateField('Ngày phát hành', validators=[DataRequired()])
    with app.app_context():
        authors = SelectMultipleField(choices=[x for x in dao.get_authors()], validators=[DataRequired()],
                                      label='Tác giả')
        categories = SelectMultipleField(choices=[x for x in dao.get_categories()], validators=[DataRequired()],
                                         label='Thể loại')
        inventories = SelectMultipleField(choices=[x for x in dao.get_inventories()], validators=[DataRequired()],
                                          label='Kho')


class CategoryForm(Form):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=1, max=50)])


class InventoryForm(Form):
    name = StringField('Inventory Name', validators=[DataRequired(), Length(min=1, max=50)])
