import pytest
import sys, os

# Make sure library_service.py can be found
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from library_service import add_book_to_catalog, borrow_book_by_patron


# ---------- Testing add_book_to_catalog ----------

def test_add_book_success(monkeypatch):
    # mock database: ISBN does not exist, insert successful
    monkeypatch.setattr("database.get_book_by_isbn", lambda isbn: None)
    monkeypatch.setattr("database.insert_book", lambda *args, **kwargs: True)

    success, msg = add_book_to_catalog("Python Basics", "Guido", "1234567890123", 3)
    assert success is True
    assert "successfully added" in msg.lower()


def test_add_book_duplicate(monkeypatch):
    # mock database: ISBN already exists
    monkeypatch.setattr("database.get_book_by_isbn", lambda isbn: {"id": 1})
    monkeypatch.setattr("database.insert_book", lambda *args, **kwargs: True)

    success, msg = add_book_to_catalog("Python Basics", "Guido", "1234567890123", 3)
    assert success is False
    assert "already exists" in msg.lower()


def test_add_book_invalid_input():
   # No need to mock database, trigger input errors directly
    success, msg = add_book_to_catalog("", "Guido", "1234567890123", 3)
    assert success is False
    assert "title is required" in msg.lower()

    success, msg = add_book_to_catalog("Python Basics", "", "1234567890123", 3)
    assert success is False
    assert "author is required" in msg.lower()
import pytest
import sys, os

# Make sure library_service.py can be found
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from library_service import add_book_to_catalog, borrow_book_by_patron


# ---------- Testing add_book_to_catalog ----------

def test_add_book_success(monkeypatch):
    monkeypatch.setattr("library_service.get_book_by_isbn", lambda isbn: None)
    monkeypatch.setattr("library_service.insert_book", lambda *args, **kwargs: True)

    success, msg = add_book_to_catalog("Python Basics", "Guido", "1234567890123", 3)
    assert success is True
    assert "successfully added" in msg.lower()


def test_add_book_duplicate(monkeypatch):
    monkeypatch.setattr("library_service.get_book_by_isbn", lambda isbn: {"id": 1})
    monkeypatch.setattr("library_service.insert_book", lambda *args, **kwargs: True)

    success, msg = add_book_to_catalog("Python Basics", "Guido", "1234567890123", 3)
    assert success is False
    assert "already exists" in msg.lower()


def test_add_book_invalid_input():
    success, msg = add_book_to_catalog("", "Guido", "1234567890123", 3)
    assert success is False
    assert "title is required" in msg.lower()

    success, msg = add_book_to_catalog("Python Basics", "", "1234567890123", 3)
    assert success is False
    assert "author is required" in msg.lower()

    success, msg = add_book_to_catalog("Python Basics", "Guido", "12345", 3)
    assert success is False
    assert "isbn must be exactly 13 digits" in msg.lower()

    success, msg = add_book_to_catalog("Python Basics", "Guido", "1234567890123", -1)
    assert success is False
    assert "positive integer" in msg.lower()


# ---------- Testing borrow_book_by_patron ----------

def test_borrow_success(monkeypatch):
    fake_book = {"id": 1, "title": "Python Basics", "available_copies": 2}

    monkeypatch.setattr("library_service.get_book_by_id", lambda book_id: fake_book)
    monkeypatch.setattr("library_service.get_patron_borrow_count", lambda patron_id: 1)
    monkeypatch.setattr("library_service.insert_borrow_record", lambda *args, **kwargs: True)
    monkeypatch.setattr("library_service.update_book_availability", lambda *args, **kwargs: True)

    success, msg = borrow_book_by_patron("123456", 1)
    assert success is True
    assert "successfully borrowed" in msg.lower()


def test_borrow_invalid_patron():
    success, msg = borrow_book_by_patron("abc", 1)
    assert success is False
    assert "invalid patron id" in msg.lower()


def test_borrow_book_not_found(monkeypatch):
    monkeypatch.setattr("library_service.get_book_by_id", lambda book_id: None)

    success, msg = borrow_book_by_patron("123456", 1)
    assert success is False
    assert "book not found" in msg.lower()


def test_borrow_no_copies(monkeypatch):
    fake_book = {"id": 1, "title": "Python Basics", "available_copies": 0}
    monkeypatch.setattr("library_service.get_book_by_id", lambda book_id: fake_book)

    success, msg = borrow_book_by_patron("123456", 1)
    assert success is False
    assert "not available" in msg.lower()


def test_borrow_limit_exceeded(monkeypatch):
    fake_book = {"id": 1, "title": "Python Basics", "available_copies": 2}
    monkeypatch.setattr("library_service.get_book_by_id", lambda book_id: fake_book)
    monkeypatch.setattr("library_service.get_patron_borrow_count", lambda patron_id: 6)

    success, msg = borrow_book_by_patron("123456", 1)
    assert success is False
    assert "maximum borrowing limit" in msg.lower()
