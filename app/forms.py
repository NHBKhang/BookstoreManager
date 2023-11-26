from wtforms import Form, StringField, BooleanField, IntegerField, TextAreaField, DateField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, Email
from app import dao, app


class AuthorForm(Form):
    name = StringField('Tên tác giả', validators=[DataRequired(), Length(min=1, max=50)])


class BookViewForm(Form):
    name = StringField('Tên sách', validators=[DataRequired(), Length(min=1, max=50)])
    price = IntegerField('Giá', validators=[DataRequired(), NumberRange(min=1000, max=1000000)])
    active = BooleanField('Có sẵn?', validators=[DataRequired()], default=True)
    description = TextAreaField('Miêu tả', validators=[DataRequired()])
    image = StringField('Ảnh')
    published_date = DateField('Ngày phát hành', validators=[DataRequired()])
    with app.app_context():
        authors = SelectMultipleField('Tác giả', choices=[a for a in dao.get_authors()])
        categories = SelectMultipleField('Thể loại', choices=[c for c in dao.get_categories()])
        inventory = SelectField('Kho', choices=dao.get_inventories())