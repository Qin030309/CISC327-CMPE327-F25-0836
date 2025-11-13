import pytest
from services import library_service as lib

# ---- R1: add_book_to_catalog edge cases ----
def test_add_book_empty_title(mocker):
    result = lib.add_book_to_catalog("", "Author", "1234567890123", 1)
    assert result == (False, "Title is required.")

def test_add_book_long_title(mocker):
    long_title = "A" * 201
    result = lib.add_book_to_catalog(long_title, "Author", "1234567890123", 1)
    assert result[0] is False

def test_add_book_duplicate_isbn(mocker):
    mocker.patch("services.library_service.get_book_by_isbn", return_value={"isbn": "1234567890123"})
    result = lib.add_book_to_catalog("Title", "Author", "1234567890123", 1)
    assert "already exists" in result[1]


# ---- R3: borrow_book_by_patron DB failure ----
def test_borrow_book_db_failures(mocker):
    mocker.patch("services.library_service.get_book_by_id", return_value={"available_copies": 1, "title": "Book"})
    mocker.patch("services.library_service.get_patron_borrow_count", return_value=0)
    mocker.patch("services.library_service.insert_borrow_record", return_value=False)

    success, msg = lib.borrow_book_by_patron("123456", 1)
    assert success is False and "Database error" in msg


# ---- R4: return_book_by_patron missing borrow record ----
def test_return_book_not_borrowed(mocker):
    mocker.patch("services.library_service.get_book_by_id", return_value={"book_id": 1, "title": "Book"})
    mocker.patch("services.library_service.get_patron_borrowed_books", return_value=[])
    success, msg = lib.return_book_by_patron("123456", 1)
    assert success is False and "not borrowed" in msg


# ---- R5: calculate_late_fee edge cases ----
def test_calculate_fee_no_record(mocker):
    mocker.patch("services.library_service.get_patron_borrowed_books", return_value=[])
    result = lib.calculate_late_fee_for_book("123456", 1)
    assert result["status"].startswith("No active")

def test_calculate_fee_overdue(mocker):
    from datetime import datetime, timedelta
    overdue = datetime.now() - timedelta(days=10)
    mocker.patch("services.library_service.get_patron_borrowed_books", return_value=[
        {"book_id": 1, "due_date": overdue, "return_date": None}
    ])
    result = lib.calculate_late_fee_for_book("123456", 1)
    assert result["fee_amount"] > 0


# ---- R6: invalid search type ----
def test_search_invalid_type(mocker):
    mocker.patch("services.library_service.get_all_books", return_value=[])
    result = lib.search_books_in_catalog("test", "unknown")
    assert result == []


# ---- refund_late_fee_payment edge cases ----
def test_refund_invalid_inputs(mocker):
    gateway = mocker.Mock()
    # Invalid transaction_id
    assert lib.refund_late_fee_payment("", 5.0, gateway) == (False, "Invalid transaction ID.")
    # Invalid amount <= 0
    assert lib.refund_late_fee_payment("tx1", 0, gateway)[0] is False
    # Invalid amount > 15
    assert lib.refund_late_fee_payment("tx1", 20, gateway)[0] is False

def test_refund_gateway_failure(mocker):
    gateway = mocker.Mock()
    gateway.refund_payment.return_value = {"status": "failed", "reason": "declined"}
    success, msg = lib.refund_late_fee_payment("tx1", 5.0, gateway)
    assert not success and "declined" in msg
