from services import library_service as ls
from services import payment_service as ps

def test_insert_book_minimal():
    # 最小化测试 insert_book
    result = ls.insert_book({"book_id": 999, "title": "Test Book"})
    assert result is not None

def test_insert_borrow_record_minimal():
    # 最小化测试 insert_borrow_record
    result = ls.insert_borrow_record({"patron_id": "p1", "book_id": 999})
    assert result is not None

def test_reset_globals_minimal():
    # 直接调用 reset_globals，不使用 fixture
    ls.reset_globals()
    # 只验证可以调用，不断言具体内容

def test_get_catalog_minimal():
    # 调用 get_catalog
    _ = ls.get_catalog()

def test_get_borrowed_books_minimal():
    # 调用 get_borrowed_books
    _ = ls.get_borrowed_books()

def test_get_patron_borrowed_books_minimal():
    # 调用 get_patron_borrowed_books
    _ = ls.get_patron_borrowed_books("p1")

def test_pay_and_refund_minimal():
    # 创建 PaymentGateway 实例
    gateway = ps.PaymentGateway()
    # pay_late_fees 最小化调用
    ls.pay_late_fees("p1", 5.0, gateway)
    # refund_late_fee_payment 最小化调用
    ls.refund_late_fee_payment("tx123", 5.0, gateway)
