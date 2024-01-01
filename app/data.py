from datetime import datetime
from app import db, dao, models, app


def add_accounts():
    from app.models import Admin, Customer, Staff
    import hashlib

    admin = Admin(username='admin', password=hashlib.md5("123456".encode('utf-8')).hexdigest(), name='admin',
                  email='admin@gmail.com')
    db.session.add_all([admin])
    customer = Customer(username='khang', name='khang', password=hashlib.md5('khang2003'.encode('utf-8')).hexdigest(),
                        email='2151053027khang@ou.edu.vn', phone='0123456789', first_name='Khang', last_name='Nguyễn',
                        birthday=datetime.strptime('29/01/2003', '%d/%m/%Y'), address='11 HCS, Bến Lức, Long An')
    db.session.add_all([customer])
    staff = Staff(username='huyshipping', name='huy', password=hashlib.md5('11001100'.encode('utf-8')).hexdigest(),
                  email='huyshipping@gmail.com', phone='0123456999', first_name='Huy', last_name='Phan',
                  birthday=datetime.strptime('21/11/2000', '%d/%m/%Y'), address='TTT, Q12, Tp HCM',
                  job_title=models.StaffJobTitle.SHIPPING)
    db.session.add_all([staff])
    db.session.commit()


def add_categories():
    from app.models import Category

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
    c15 = Category(name='Thể thao')
    c16 = Category(name='Âm nhạc')
    db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16])
    db.session.commit()


def add_inventory():
    from app.models import Inventory

    inventory = Inventory(name='Kho 1')
    db.session.add(inventory)
    db.session.commit()


def add_book_categories(book_id, category_ids):
    for id in category_ids:
        dao.add_book_category(book_id, id)


def add_book_authors(book_id, author_ids):
    for id in author_ids:
        dao.add_book_author(book_id, id)


def add_authors():
    from app.models import Author
    a1 = Author(name='Anne Rice')
    a2 = Author(name='Alix E. Harrow')
    a3 = Author(name='Jana Monroe')
    a4 = Author(name='Tappei Nagatsuki')
    a5 = Author(name='Brenna Thummler')
    a6 = Author(name='Anna Pitoniak')
    a7 = Author(name='Walter Isaacson')
    a8 = Author(name='Susannah Breslin')
    a9 = Author(name='Beth Santos')
    a10 = Author(name='Axie Oh')
    a11 = Author(name='')
    db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10])
    db.session.commit()


def add_books():
    dao.add_book('The Wolf Gift', 250000,
                 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1328214020i/12880428.jpg',
                 'Nơi có bờ biển gồ ghề phía bắc California. Một trò lừa đảo cao trên Thái Bình Dương. Một dinh thự hoành tráng đầy vẻ đẹp và lịch sử đầy trêu ngươi nằm đối diện với khu rừng gỗ đỏ cao chót vót.',
                 '2012-12-14')
    add_book_authors(1, [1])  # add author trc
    dao.add_book_inventory(1)
    add_book_categories(1, [1, 2, 12])

    dao.add_book('Starling House', 300000,
                 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1682447293i/65213595.jpg',
                 'Một câu chuyện mới đầy nghiệt ngã và kiểu gothic của tác giả Alix E. Harrow về một thị trấn nhỏ bị ám ảnh bởi những bí mật không thể chôn vùi và ngôi nhà nham hiểm nằm ở ngã tư của tất cả.',
                 '2023-10-10')
    add_book_authors(2, [2])
    dao.add_book_inventory(2)
    add_book_categories(2, [1, 4, 7, 12])

    dao.add_book('Hearts of Darkness', 320000,
                 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1679147652i/98653090.jpg',
                 'Dành cho những người hâm mộ Mindhunter, Crime Minds và My Favorite Murder, một cuốn hồi ký hấp dẫn về cuộc đời của một người phụ nữ tiên phong săn lùng những kẻ giết người hàng loạt với tư cách là một trong những nữ lập hồ sơ đầu tiên của Đơn vị Khoa học Hành vi FBI.',
                 '2023-10-10')
    add_book_authors(3, [3])
    dao.add_book_inventory(3)
    add_book_categories(3, [3])

    dao.add_book('Re:ZERO', 120000,
                 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1498758856i/28603205.jpg',
                 'Subaru Natsuki đang cố gắng đến cửa hàng tiện lợi nhưng cuối cùng lại bị triệu hồi đến một thế giới khác. Tất cả những điều đó đã đủ tệ rồi, nhưng anh ấy cũng có được khả năng ma thuật bất tiện nhất mọi thời đại - du hành thời gian, nhưng anh ấy phải chết để sử dụng nó. Làm thế nào để bạn trả ơn người đã cứu mạng bạn khi tất cả những gì bạn có thể làm là chết?',
                 '2014-01-24')
    add_book_authors(4, [4])
    dao.add_book_inventory(4)
    add_book_categories(4, [1, 6, 7, 12])

    dao.add_book('Sheets', 125000,
                 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1529034024i/38958846.jpg',
                 'Marjorie Glatt cảm thấy mình như một bóng ma. Một cô bé mười ba tuổi thực tế phụ trách công việc kinh doanh giặt là của gia đình, công việc hàng ngày của cô có những khách hàng không thể tha thứ, những P.E. khó chịu. và ông Saubertuck khó tính, người cam kết phá hủy mọi thứ mà cô ấy đã làm việc.',
                 '2014-01-23')
    add_book_authors(5, [5])
    dao.add_book_inventory(5)
    add_book_categories(5, [1, 5, 9])

    dao.add_book('The Helsinki Affair', 210000,
                 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1676130404i/101145039.jpg',
                 'Đặc vụ CIA Amanda Cole bị đẩy vào một âm mưu quốc tế liên quan đến các vụ ám sát cấp cao và tống tiền của Nga. Đó là trường hợp của cuộc đời cô, nhưng việc giải quyết nó có thể đòi hỏi cô phải phản bội một điệp viên khác - người tình cờ lại chính là cha cô.',
                 '2014-11-14')
    add_book_authors(6, [6])
    dao.add_book_inventory(6)
    add_book_categories(6, [1, 13])

    dao.add_book('Elon Musk', 350000,
                 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1692288251i/122765395.jpg',
                 'Từ tác giả cuốn Steve Jobs và những cuốn tiểu sử bán chạy khác, đây là câu chuyện sâu sắc đến kinh ngạc về nhà đổi mới hấp dẫn và gây tranh cãi nhất trong thời đại chúng ta - một người có tầm nhìn phá vỡ các quy tắc, người đã giúp dẫn dắt thế giới vào kỷ nguyên xe điện, khám phá không gian riêng tư, và trí tuệ nhân tạo. Ồ, và đã chiếm lĩnh Twitter.',
                 '2014-12-10')
    add_book_authors(7, [7])
    dao.add_book_inventory(7)
    add_book_categories(7, [3, 14])

    dao.add_book('Data Baby', 270000,
                 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1659417016i/61237017.jpg',
                 'Điều gì sẽ xảy ra nếu cha mẹ bạn biến bạn thành chuột thí nghiệm vào ngày bạn được sinh ra? Điều đó có thay đổi câu chuyện cuộc đời bạn không? Liệu điều đó có thay đổi con người bạn không?',
                 '2023-11-07')
    add_book_authors(8, [8])  # add author trc
    dao.add_book_inventory(8)
    add_book_categories(8, [10])

    dao.add_book('Wander Woman', 225000,
                 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1684209959i/145624885.jpg',
                 'Đạt được ước mơ du lịch một mình dành cho nữ giới của bạn với hướng dẫn đầy sức mạnh này dành cho những phụ nữ muốn nhìn ngắm thế giới—hoàn hảo cho bất kỳ ai cảm thấy khao khát lang thang sau khi đọc Wild, Eat Pray Love hoặc What I Was doing When You Were Breeding.',
                 '2024-05-05')
    add_book_authors(9, [9])  # add author trc
    dao.add_book_inventory(9)
    add_book_categories(9, [8])

    dao.add_book('XOXO', 150000,
                 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1602086642i/54618808.jpg',
                 'Thần đồng cello Jenny có một mục tiêu: vào được một nhạc viện danh tiếng. Khi cô gặp Jaewoo đẹp trai, bí ẩn trong quán karaoke ở Los Angeles của chú cô, rõ ràng anh là kiểu con trai sẽ phá bỏ những kế hoạch cẩn thận của cô. Nhưng trong một khoảnh khắc tự phát, cô cho phép anh kéo cô ra khỏi vùng an toàn của mình để có một đêm phiêu lưu khó quên… trước khi anh biến mất không một lời nói.',
                 '2021-07-13')
    add_book_authors(10, [10])  # add author trc
    dao.add_book_inventory(10)
    add_book_categories(10, [1, 7, 16])


def add_orders():
    dao.add_order(customer_id=2, is_paid=True)
    dao.add_order_details(1, 1, 240000, 1)
    dao.add_order_details(1, 4, 105000, 1)
    dao.add_order(created_date=datetime.strptime('2023-12-20 17:03:02', '%Y-%m-%d %H:%M:%S'), customer_id=2)
    dao.add_order_details(2, 5, 125000, 2)


def add_receipts():
    dao.add_receipt(customer_id=2, staff_id=3)
    dao.add_receipt_details(quantity=1, price=240000, receipt_id=1, book_id=1)

    dao.add_receipt(customer_id=2, staff_id=3)
    dao.add_receipt_details(quantity=2, receipt_id=2, book_id=7)
    dao.add_receipt_details(quantity=1, receipt_id=2, book_id=3)

    dao.add_receipt(customer_id=2, staff_id=3)
    dao.add_receipt_details(quantity=2, receipt_id=3, book_id=10)
    dao.add_receipt_details(quantity=1, receipt_id=3, book_id=1)
    dao.add_receipt_details(quantity=2, receipt_id=3, book_id=4)


if __name__ == '__main__':
    with app.app_context():
        add_accounts()

        add_categories()

        add_inventory()

        add_authors()

        add_books()

        add_orders()

        add_receipts()
