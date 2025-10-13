import pytest
from library_service import add_book_to_catalog
import random

def unique_isbn():
    """Generate a unique 13-character ISBN (digits or letters, matches current R1)"""
    return str(random.randint(10**12, 10**13 - 1))

# -------------------------
# Valid Input Tests
# -------------------------
def test_add_book_valid_input():
    """Valid books should be successfully added"""
    for _ in range(3):
        isbn = unique_isbn()
        success, message = add_book_to_catalog(
            "Test Book", "Test Author", isbn, 5
        )
        assert success is True
        assert "successfully" in message.lower()


# -------------------------
# Title Validation
# -------------------------
def test_add_book_empty_title():
    """Empty title should fail"""
    isbn = unique_isbn()
    success, message = add_book_to_catalog("", "Test Author", isbn, 5)
    assert success is False
    assert "title" in message.lower()


def test_add_book_title_too_long():
    """Title exceeding 200 chars should fail"""
    for length in [201, 250]:
        isbn = unique_isbn()
        long_title = "A" * length
        success, message = add_book_to_catalog(long_title, "Test Author", isbn, 5)
        assert success is False
        assert "title" in message.lower()


def test_add_book_title_edge():
    """Title exactly 200 chars should pass"""
    isbn = unique_isbn()
    long_title = "A" * 200
    success, message = add_book_to_catalog(long_title, "Test Author", isbn, 5)
    assert success is True


# -------------------------
# Author Validation
# -------------------------
def test_add_book_empty_author():
    """Empty author should fail"""
    isbn = unique_isbn()
    success, message = add_book_to_catalog("Valid Title", "", isbn, 5)
    assert success is False
    assert "author" in message.lower()


def test_add_book_author_too_long():
    """Author exceeding 100 chars should fail"""
    for length in [101, 120]:
        isbn = unique_isbn()
        long_author = "B" * length
        success, message = add_book_to_catalog("Valid Title", long_author, isbn, 5)
        assert success is False
        assert "author" in message.lower()


def test_add_book_author_edge():
    """Author exactly 100 chars should pass"""
    isbn = unique_isbn()
    long_author = "B" * 100
    success, message = add_book_to_catalog("Valid Title", long_author, isbn, 5)
    assert success is True


# -------------------------
# ISBN Validation
# -------------------------
def test_add_book_isbn_valid():
    """13-char ISBN should pass"""
    isbn = unique_isbn()
    success, message = add_book_to_catalog("Valid Title", "Valid Author", isbn, 5)
    assert success is True


def test_add_book_isbn_invalid_length():
    """ISBN with length != 13 should fail"""
    for isbn in ["123456789012", "12345678901234"]:
        success, message = add_book_to_catalog("Valid Title", "Valid Author", isbn, 5)
        assert success is False
        assert "ISBN" in message


def test_add_book_isbn_non_digit():
    """Currently non-digit ISBN of length 13 passes according to R1"""
    isbn = "ABCDEFGHIJKLM"
    success, message = add_book_to_catalog("Valid Title", "Valid Author", isbn, 5)
    assert success is True
    assert "successfully" in message.lower()


# -------------------------
# Total Copies Validation
# -------------------------
def test_add_book_total_copies_invalid():
    """Negative or zero total copies should fail"""
    for copies in [-1, 0, -10]:
        isbn = unique_isbn()
        success, message = add_book_to_catalog("Valid Title", "Valid Author", isbn, copies)
        assert success is False
        assert "total copies" in message.lower()


def test_add_book_total_copies_valid():
    """Positive total copies should pass"""
    for copies in [1, 5, 100, 1000]:
        isbn = unique_isbn()
        success, message = add_book_to_catalog("Valid Title", "Valid Author", isbn, copies)
        assert success is True
        assert "successfully" in message.lower()

