# tests/test_add_book_R1_complete.py
import pytest
from library_service import add_book_to_catalog, clear_catalog

@pytest.fixture(autouse=True)
def reset_catalog():
    """每个测试前清空 catalog"""
    clear_catalog()

# -------------------------
# 成功添加书籍
# -------------------------
def test_add_book_valid_input():
    success, message = add_book_to_catalog(
        "A Good Book", "Some Author", "1234567890123", 5
    )
    assert success
    assert "successfully added" in message.lower()

# -------------------------
# 标题相关边界
# -------------------------
def test_add_book_empty_title():
    success, message = add_book_to_catalog("", "Some Author", "1234567890123", 5)
    assert not success
    assert "title is required" in message.lower()

def test_add_book_title_too_long():
    long_title = "A" * 201
    success, message = add_book_to_catalog(long_title, "Some Author", "1234567890123", 5)
    assert not success
    assert "less than 200" in message.lower()

def test_add_book_title_edge():
    edge_title = "A" * 200
    success, message = add_book_to_catalog(edge_title, "Some Author", "1234567890123", 5)
    assert success

# -------------------------
# 作者相关边界
# -------------------------
def test_add_book_empty_author():
    success, message = add_book_to_catalog("A Good Book", "", "1234567890123", 5)
    assert not success
    assert "author is required" in message.lower()

def test_add_book_author_too_long():
    long_author = "B" * 101
    success, message = add_book_to_catalog("A Good Book", long_author, "1234567890123", 5)
    assert not success
    assert "less than 100" in message.lower()

def test_add_book_author_edge():
    edge_author = "B" * 100
    success, message = add_book_to_catalog("A Good Book", edge_author, "1234567890123", 5)
    assert success

# -------------------------
# ISBN 验证
# -------------------------
def test_add_book_isbn_valid():
    isbn = "1234567890123"
    success, message = add_book_to_catalog("A Good Book", "Some Author", isbn, 5)
    assert success

def test_add_book_isbn_invalid_length():
    success, message = add_book_to_catalog("A Good Book", "Some Author", "1234567", 5)
    assert not success
    assert "isbn must be exactly 13" in message.lower()

# -------------------------
# Total copies 验证
# -------------------------
def test_add_book_total_copies_invalid():
    success, message = add_book_to_catalog("A Good Book", "Some Author", "1234567890123", 0)
    assert not success
    assert "positive integer" in message.lower()

def test_add_book_total_copies_valid():
    success, message = add_book_to_catalog("A Good Book", "Some Author", "1234567890123", 1)
    assert success

# -------------------------
# 重复 ISBN
# -------------------------
def test_add_book_duplicate_isbn():
    add_book_to_catalog("Book 1", "Author 1", "1234567890123", 1)
    success, message = add_book_to_catalog("Book 2", "Author 2", "1234567890123", 2)
    assert not success
    assert "already exists" in message.lower()



