import pytest
from datetime import datetime, timedelta
from library_service import (
    add_book_to_catalog,
    borrow_book_by_patron,
    return_book_by_patron,
    calculate_late_fee_for_book,
    search_books_in_catalog,
    get_patron_status_report
)

# =====================================
# R1: Add Book To Catalog Tests
# =====================================
def test_add_book_valid():
    success, message = add_book_to_catalog("Valid Book", "Valid Author", "1234567890123", 5)
    assert success
    assert "successfully added" in message.lower()

def test_add_book_empty_title():
    success, message = add_book_to_catalog("", "Author", "1234567890123", 1)
    assert not success
    assert "title is required" in message.lower()

def test_add_book_title_too_long():
    title = "A" * 201
    success, message = add_book_to_catalog(title, "Author", "1234567890123", 1)
    assert not success
    assert "less than 200" in message.lower()

def test_add_book_empty_author():
    success, message = add_book_to_catalog("Book", "", "1234567890123", 1)
    assert not success
    assert "author is required" in message.lower()

def test_add_book_author_too_long():
    author = "B" * 101
    success, message = add_book_to_catalog("Book", author, "1234567890123", 1)
    assert not success
    assert "less than 100" in message.lower()

def test_add_book_invalid_isbn_length():
    success, message = add_book_to_catalog("Book", "Author", "12345", 1)
    assert not success
    assert "13 digits" in message.lower()

def test_add_book_negative_total_copies():
    success, message = add_book_to_catalog("Book", "Author", "1234567890123", -5)
    assert not success
    assert "positive integer" in message.lower()

# =====================================
# R3: Borrow Book Tests
# =====================================
def test_borrow_book_valid():
    success, message = borrow_book_by_patron("123456", 1)
    assert success
    assert "successfully borrowed" in message.lower()

def test_borrow_book_invalid_patron_non_digit():
    success, message = borrow_book_by_patron("abc123", 1)
    assert not success
    assert "invalid patron" in message.lower()

def test_borrow_book_invalid_patron_length():
    success, message = borrow_book_by_patron("12345", 1)
    assert not success
    assert "invalid patron" in message.lower()

def test_borrow_book_no_copies():
    # Assume book_id=2 has 0 available copies
    success, message = borrow_book_by_patron("123456", 2)
    assert not success
    assert "not available" in message.lower()

def test_borrow_book_exceed_limit():
    # Assume patron "999999" already borrowed 5 books
    success, message = borrow_book_by_patron("999999", 1)
    assert not success
    assert "maximum borrowing limit" in message.lower()

# =====================================
# R4: Return Book Tests
# =====================================
def test_return_book_not_borrowed():
    success, message = return_book_by_patron("123456", 99)
    assert not success
    assert "no active borrow record" in message.lower()

def test_return_book_on_time():
    # Assume book was borrowed on time
    success, message = return_book_by_patron("123456", 1)
    assert success
    assert "no late fee" in message.lower()

def test_return_book_overdue_less_than_7():
    # Manually adjust borrow date in database if needed
    success, message = return_book_by_patron("123456", 3)
    assert success
    assert "late fee" in message.lower()
    assert "$" in message

def test_return_book_overdue_more_than_7():
    # Assume book was borrowed >7 days overdue
    success, message = return_book_by_patron("123456", 4)
    assert success
    assert "late fee" in message.lower()
    assert "$" in message

# =====================================
# R5: Late Fee Calculation Tests
# =====================================
def test_late_fee_not_overdue():
    fee_info = calculate_late_fee_for_book("123456", 1)
    assert fee_info["fee_amount"] == 0
    assert fee_info["days_overdue"] == 0

def test_late_fee_overdue_5_days():
    fee_info = calculate_late_fee_for_book("123456", 3)
    assert fee_info["fee_amount"] == 5 * 0.50  # 5 days within first 7
    assert fee_info["days_overdue"] == 5

def test_late_fee_overdue_10_days():
    fee_info = calculate_late_fee_for_book("123456", 4)
    # 7 days * 0.5 + 3 days * 1.0
    assert fee_info["fee_amount"] == 7 * 0.5 + 3 * 1.0
    assert fee_info["days_overdue"] == 10

def test_late_fee_capped_at_15():
    fee_info = calculate_late_fee_for_book("123456", 5)
    assert fee_info["fee_amount"] <= 15.0

# =====================================
# R6: Search Functionality Tests
# =====================================
def test_search_by_title_partial():
    results = search_books_in_catalog("Test", "title")
    assert isinstance(results, list)
    for book in results:
        assert "test" in book["title"].lower()

def test_search_by_author_partial():
    results = search_books_in_catalog("Author", "author")
    assert isinstance(results, list)
    for book in results:
        assert "author" in book["author"].lower()

def test_search_by_isbn_exact():
    results = search_books_in_catalog("1234567890123", "isbn")
    assert len(results) == 1
    assert results[0]["isbn"] == "1234567890123"

def test_search_empty_query():
    results = search_books_in_catalog("", "title")
    assert results == []

def test_search_invalid_type():
    results = search_books_in_catalog("Test", "invalid")
    assert results == []

# =====================================
# R7: Patron Status Report Tests
# =====================================
def test_patron_status_report_basic():
    report = get_patron_status_report("123456")
    assert "current_borrowed" in report
    assert "borrow_history" in report
    assert isinstance(report["current_borrowed"], list)
    assert isinstance(report["borrow_history"], list)

def test_patron_status_report_late_fees():
    report = get_patron_status_report("123456")
    total_fee_calculated = sum([book["late_fee"] for book in report["current_borrowed"]])
    assert round(report["total_late_fees"], 2) == round(total_fee_calculated, 2)
