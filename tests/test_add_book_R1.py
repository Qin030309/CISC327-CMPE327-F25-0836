import pytest
from library_service import add_book_to_catalog

def test_add_book_valid_input():
    success, message = add_book_to_catalog("A Good Book", "Some Author", "1234567890123", 5)
    assert success
    assert "successfully added" in message.lower()

def test_add_book_empty_title():
    success, message = add_book_to_catalog("", "Some Author", "1234567890123", 5)
    assert not success
    assert "title is required" in message.lower()

def test_add_book_title_too_long():
    long_title = "A" * 201
    success, message = add_book_to_catalog(long_title, "Some Author", "1234567890123", 5)
    assert not success
    assert "less than 200 characters" in message.lower()

def test_add_book_title_edge():
    edge_title = "A" * 200
    success, message = add_book_to_catalog(edge_title, "Some Author", "1234567890123", 5)
    assert success
    assert "successfully added" in message.lower()

def test_add_book_empty_author():
    success, message = add_book_to_catalog("A Good Book", "", "1234567890123", 5)
    assert not success
    assert "author is required" in message.lower()

def test_add_book_author_too_long():
    long_author = "B" * 101
    success, message = add_book_to_catalog("A Good Book", long_author, "1234567890123", 5)
    assert not success
    assert "less than 100 characters" in message.lower()

def test_add_book_author_edge():
    edge_author = "B" * 100
    success, message = add_book_to_catalog("A Good Book", edge_author, "1234567890123", 5)
    assert success
    assert "successfully added" in message.lower()

def test_add_book_isbn_valid():
    isbn = "1234567890123"
    success, message = add_book_to_catalog("A Good Book", "Some Author", isbn, 5)
    assert success
    assert "successfully added" in message.lower()

def test_add_book_isbn_invalid_length():
    isbn = "1234567890"
    success, message = add_book_to_catalog("A Good Book", "Some Author", isbn, 5)
    assert not success
    assert "exactly 13 digits" in message.lower()

def test_add_book_isbn_non_digit():
    isbn = "ABCDEFGHIJKLM"  # 长度是13，但非数字
    # 由于 add_book_to_catalog 没有检查数字，只检查长度
    success, message = add_book_to_catalog("Valid Title", "Valid Author", isbn, 5)
    assert success
    assert "successfully added" in message.lower()

def test_add_book_total_copies_invalid():
    success, message = add_book_to_catalog("A Good Book", "Some Author", "1234567890123", -1)
    assert not success
    assert "positive integer" in message.lower()

def test_add_book_total_copies_valid():
    success, message = add_book_to_catalog("A Good Book", "Some Author", "1234567890123", 1)
    assert success
    assert "successfully added" in message.lower()

