from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from app import db, app
from datetime import datetime
from flask_login import UserMixin
import enum


class GenderType(enum.Enum):
    MALE = 1,
    FEMALE = 2


class AccountStatus(enum.Enum):
    ACTIVE = 1,
    BANNED = 2


class AdminRole(enum.Enum):
    OWNER = 1


class Category(db.Model):
    __tablename__ = 'category'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    books = relationship('Book_Category', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Author(db.Model):
    __tablename__ = 'author'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    books = relationship('Book_Author', backref='author', lazy=True)

    def __str__(self):
        return self.name


class Inventory(db.Model):
    __tablename__ = 'inventory'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)

    def __str__(self):
        return self.name


class Book(db.Model):
    __tablename__ = 'book'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    price = Column(Integer, default=0)
    image = Column(String(255),
                   default='https://www.google.com/url?sa=i&url=https%3A%2F%2Fstock.adobe.com%2Fsearch%3Fk%3Dnth&psig=AOvVaw2ikijy0zik25q-f-qDM3gL&ust=1700653615974000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCJja38aC1YIDFQAAAAAdAAAAABAE')
    active = Column(Boolean, default=True)
    description = Column(String(512), nullable=False)
    authors = relationship("Book_Author", backref='book', lazy=True)
    published_date = Column(DateTime, nullable=False)
    categories = relationship("Book_Category", backref='book')
    inventories = relationship("Book_Inventory", backref='book', lazy=True)

    def __str__(self):
        return self.name


class Book_Category(db.Model):
    __tablename__ = 'book_category'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)


class Book_Author(db.Model):
    __tablename__ = 'book_author'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)


class Book_Inventory(db.Model):
    __tablename__ = 'book_inventory'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    inventory_id = Column(Integer, ForeignKey(Inventory.id), nullable=False, default=1)
    quantity = Column(Integer, nullable=False)
    added_date = Column(DateTime, nullable=False, default=datetime.now())


class Account(db.Model, UserMixin):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    avatar = Column(String(255), nullable=False,
                    default='https://e7.pngegg.com/pngimages/799/987/png-clipart-computer-icons-avatar-icon-design-avatar-heroes-computer-wallpaper-thumbnail.png')
    register_date = Column(DateTime, default=datetime.now())
    last_login = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Admin(Account):
    __tablename__ = 'admin'
    __table_args__ = {'extend_existing': True}

    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(Enum(AdminRole), default=AdminRole.OWNER)


class User(Account):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birthday = Column(DateTime, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(12), unique=True, nullable=False)
    gender = Column(Enum(GenderType), nullable=False, default=GenderType.MALE)
    address = Column(String(100), nullable=False)


def add_accounts():
    import hashlib
    admin = Admin(username='admin', password=hashlib.md5("123456".encode('utf-8')).hexdigest(), name='admin',
                  email='admin@gmail.com')
    db.session.add_all([admin])
    db.session.commit()
def add_categories():
    c1 = Category(name='Viễn tưởng')
    c2 = Category(name='Kinh dị')
    c3 = Category(name="Lịch sử")
    c4 = Category(name="Nghệ thuật")
    c5 = Category(name="Truyện tranh")
    c6 = Category(name="Light novel")
    c7 = Category(name="Lãng mạn")
    c8 = Category(name="Du lịch")
    c9 = Category(name="Trẻ em")
    c10 = Category(name="Khoa học")
    c11 = Category(name="Hài hước")
    c12 = Category(name="Tưởng tượng")
    c13 = Category(name="Người lớn")
    c14 = Category(name="Công nghệ")
    db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14])
    db.session.commit()
def add_inventory():
    inventory = Inventory(name='Kho 1')
    db.session.add(inventory)
    db.session.commit()
def add_authors():
    a1 = Author(name='Anne Rice')
    a2 = Author(name='Alix E. Harrow')
    a3 = Author(name='Jana Monroe')
    a4 = Author(name='Tappei Nagatsuki')
    a5 = Author(name='Brenna Thummler')
    a6 = Author(name='Anna Pitoniak')
    a7 = Author(name='Walter Isaacson')
    # db.session.add(a7)
    db.session.add_all([a1, a2, a3, a4, a5, a6, a7])
    db.session.commit()
def add_book_author(book_id, author_ids):
    for id in author_ids:
        ba = Book_Author(book_id=book_id, author_id=id)
        db.session.add(ba)
        db.session.commit()
def add_book_inventory(book_id, inventory_id=1, quantity=100):
    bi = Book_Inventory(book_id=book_id, inventory_id=inventory_id, quantity=quantity)
    db.session.add(bi)
    db.session.commit()
def add_book_category(book_id, category_ids):
    for id in category_ids:
        bc = Book_Category(book_id=book_id, category_id=id)
        db.session.add(bc)
        db.session.commit()
def add_book(name, price, img, description, date):
    b1 = Book(name=name, price=price,
              image=img,
              description=description,
              published_date=datetime.strptime(date, '%d/%m/%Y'))
    db.session.add_all([b1])
    db.session.commit()
def add_books():
    add_book('The Wolf Gift', 250000, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1328214020i/12880428.jpg',
             'Nơi có bờ biển gồ ghề phía bắc California. Một trò lừa đảo cao trên Thái Bình Dương. Một dinh thự hoành tráng đầy vẻ đẹp và lịch sử đầy trêu ngươi nằm đối diện với khu rừng gỗ đỏ cao chót vót.',
             '14/12/2012')
    add_book_author(1, [1]) #add author trc
    add_book_inventory(1)
    add_book_category(1, [1, 2, 12])

    add_book('Starling House', 300000, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1682447293i/65213595.jpg',
             'Một câu chuyện mới đầy nghiệt ngã và kiểu gothic của tác giả Alix E. Harrow về một thị trấn nhỏ bị ám ảnh bởi những bí mật không thể chôn vùi và ngôi nhà nham hiểm nằm ở ngã tư của tất cả.',
             '10/10/2023')
    add_book_author(2, [2])
    add_book_inventory(2)
    add_book_category(2, [1, 4, 7, 12])

    add_book('Hearts of Darkness', 320000, 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1679147652i/98653090.jpg',
             'Dành cho những người hâm mộ Mindhunter, Crime Minds và My Favorite Murder, một cuốn hồi ký hấp dẫn về cuộc đời của một người phụ nữ tiên phong săn lùng những kẻ giết người hàng loạt với tư cách là một trong những nữ lập hồ sơ đầu tiên của Đơn vị Khoa học Hành vi FBI.',
             '10/10/2023')
    add_book_author(3, [3])
    add_book_inventory(3)
    add_book_category(3, [3])

    add_book('Re:ZERO', 120000,
             'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1498758856i/28603205.jpg',
             'Subaru Natsuki đang cố gắng đến cửa hàng tiện lợi nhưng cuối cùng lại bị triệu hồi đến một thế giới khác. Tất cả những điều đó đã đủ tệ rồi, nhưng anh ấy cũng có được khả năng ma thuật bất tiện nhất mọi thời đại - du hành thời gian, nhưng anh ấy phải chết để sử dụng nó. Làm thế nào để bạn trả ơn người đã cứu mạng bạn khi tất cả những gì bạn có thể làm là chết?',
             '23/01/2014')
    add_book_author(4, [4])
    add_book_inventory(4)
    add_book_category(4, [1, 6, 7, 12])

    add_book('Sheets', 125000,
             'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1529034024i/38958846.jpg',
             'Marjorie Glatt cảm thấy mình như một bóng ma. Một cô bé mười ba tuổi thực tế phụ trách công việc kinh doanh giặt là của gia đình, công việc hàng ngày của cô có những khách hàng không thể tha thứ, những P.E. khó chịu. và ông Saubertuck khó tính, người cam kết phá hủy mọi thứ mà cô ấy đã làm việc.',
             '23/01/2014')
    add_book_author(5, [5])
    add_book_inventory(5)
    add_book_category(5, [1, 5, 9])

    add_book('The Helsinki Affair', 210000,
             'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1676130404i/101145039.jpg',
             'Đặc vụ CIA Amanda Cole bị đẩy vào một âm mưu quốc tế liên quan đến các vụ ám sát cấp cao và tống tiền của Nga. Đó là trường hợp của cuộc đời cô, nhưng việc giải quyết nó có thể đòi hỏi cô phải phản bội một điệp viên khác - người tình cờ lại chính là cha cô.',
             '14/11/2014')
    add_book_author(6, [6])
    add_book_inventory(6)
    add_book_category(6, [1, 13])

    add_book('Elon Musk', 350000,
             'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1692288251i/122765395.jpg',
             'Từ tác giả cuốn Steve Jobs và những cuốn tiểu sử bán chạy khác, đây là câu chuyện sâu sắc đến kinh ngạc về nhà đổi mới hấp dẫn và gây tranh cãi nhất trong thời đại chúng ta - một người có tầm nhìn phá vỡ các quy tắc, người đã giúp dẫn dắt thế giới vào kỷ nguyên xe điện, khám phá không gian riêng tư, và trí tuệ nhân tạo. Ồ, và đã chiếm lĩnh Twitter.',
             '14/11/2014')
    add_book_author(7, [7])
    add_book_inventory(7)
    add_book_category(7, [3, 14])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        add_accounts()

        add_categories()

        add_inventory()

        add_authors()

        add_books()
