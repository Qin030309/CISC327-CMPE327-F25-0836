from services.library_service import *
from services.payment_service import PaymentGateway

def test_payment_gateway():
    pg = PaymentGateway()
    
    # 正常支付
    pg.process_payment(10.50)
    pg.process_payment(100.0)
    pg.process_payment(1.0)
    
    # 无效支付
    pg.process_payment(0)
    pg.process_payment(-10)
    pg.process_payment(-0.01)
    
    # 退款
    if pg.transactions:
        trans_id = list(pg.transactions.keys())[0]
        pg.refund_payment(trans_id, 5.0)
        pg.refund_payment(trans_id, 0)
        pg.refund_payment(trans_id, -1)
    
    # 无效退款
    pg.refund_payment('invalid', 10)
    pg.refund_payment('', 10)
    pg.refund_payment(None, 10)

def test_library_nuclear():
    reset_globals()
    
    for i in range(50):
        isbn = str(1000000000 + i * 123456)[:10]
        if len(isbn) == 10 and isbn.isdigit():
            add_book_to_catalog(f'Nuke{i}', f'Auth{i}', isbn, (i % 10) + 1)
    
    cat = get_catalog()
    ids = list(cat.keys())
    
    for patron_num in range(100):
        for book_id in ids[:min(len(ids), 20)]:
            borrow_book_by_patron(book_id, f'p{patron_num}')
    
    for patron_num in range(50):
        for book_id in ids[:min(len(ids), 15)]:
            return_book_by_patron(book_id, f'p{patron_num}')
    
    for patron_num in range(200):
        get_patron_borrowed_books(f'p{patron_num}')
    
    get_borrowed_books()

def test_every_error_path():
    reset_globals()
    
    errors = [
        ('', 'A', '1234567890'),
        ('T', '', '1234567890'),
        ('T', 'A', ''),
        ('T', 'A', '123'),
        ('T', 'A', '12345678901'),
        ('T', 'A', 'abcdefghij'),
        ('T'*201, 'A', '1234567890'),
        ('T', 'A'*101, '1234567890'),
        ('   ', 'A', '1234567890'),
        ('T', '   ', '1234567890'),
    ]
    
    for title, author, isbn in errors:
        add_book_to_catalog(title, author, isbn)
    
    add_book_to_catalog('T', 'A', '1234567890', 0)
    add_book_to_catalog('T', 'A', '1234567890', -1)
    
    for fake_id in ['x', 'fake', '999', '']:
        borrow_book_by_patron(fake_id, 'p')
        return_book_by_patron(fake_id, 'p')
