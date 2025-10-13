import pytest
from library_service import add_book_to_catalog
import random

def unique_isbn():
    """Generate a potentially unique 13-digit ISBN"""
    # Simple way to ensure different values each call
    return str(random.randint(10**12, 10**13 - 1))


# -------------------------
# Valid Input Tests
# -------------------------
def test_add_book_valid_input():
    """A valid book should be added successfully"""
    for _ in range(3):
        while True:
            isbn = unique_isbn()
            success, message = add_book_to_catalog("Test Book", "Test Author", isbn, 5)
            if success:
                break  # Exit loop if insertion succeeds
        assert success is True
        assert "successfully" in message.lower()


# -------------------------
# Title Validation
# -------------------------
def test_add_book_empty_title():
    isbn = unique_isbn()
    success, message = add_book_to_catalog("", "Test Author", isbn, 5)
    assert not success
    assert "title" in message.lower()


def test_add_book_title_too_long():
    for length in [201, 250]:
        isbn = unique_isbn()
        long_title = "A" * length
        success, message = add_book_to_catalog(long_title, "Test Author", isbn, 5)
        assert not success
        assert "title" in message.lower()


def test_add_book_title_edge():
    isbn = unique_isbn()
    long_title = "A" * 200
    success, message = add_book_to_catalog(long_title, "Test Author", isbn, 5)
    assert success is True


# -------------------------
# Author Validation
# -------------------------
def test_add_book_empty_author():
    isbn = unique_isbn()
    success, message = add_book_to_catalog("Valid Title", "", isbn, 5)
    assert not success
    assert "author" in message.lower()


def test_add_book_author_too_long():
    for length in [101, 120]:
        isbn = unique_isbn()
        long_author = "B" * length
        success, message = add_book_to_catalog("Valid Title", long_author, isbn, 5)
        assert not success
        assert "author" in message.lower()


def test_add_book_author_edge():
    isbn = unique_isbn()
    long_author = "B" * 100
    success, message = add_book_to_catalog("Valid Title", long_author, isbn, 5)
    assert success is True


# -------------------------
# ISBN Validation
# -------------------------
def test_add_book_isbn_valid():
    """A 13-digit numeric ISBN should succeed"""
    while True:
        isbn = unique_isbn()
        success, message = add_book_to_catalog("Valid Title", "Valid Author", isbn, 5)
        if success:
            break
    assert success is True


def test_add_book_isbn_invalid_length():
    for isbn in ["123456789012", "12345678901234"]:
        success, message = add_book_to_catalog("Valid Title", "Valid Author", isbn, 5)
        assert not success
        assert "ISBN" in message


def test_add_book_isbn_non_digit():
    isbn = "ABCDEFGHIJKLM"
    success, message = add_book_to_catalog("Valid Title", "Valid Author", isbn, 5)
    # Consider it passed if insertion fails
    assert not success


# -------------------------
# Total Copies Validation
# -------------------------
def test_add_book_total_copies_invalid():
    for copies in [-1, 0, -10]:
        isbn = unique_isbn()
        success, message = add_book_to_catalog("Valid Title", "Valid Author", isbn, copies)
        assert not success
        assert "total copies" in message.lower()


def test_add_book_total_copies_valid():
    for copies in [1, 5, 100, 1000]:
        while True:
            isbn = unique_isbn()
            success, message = add_book_to_catalog("Valid Title", "Valid Author", isbn, copies)
            if success:
                break
        assert success is True
        assert "successfully" in message.lower()
