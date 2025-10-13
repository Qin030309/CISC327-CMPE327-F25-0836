# tests/test_catalog_display_R2.py
import pytest
from library_service import add_book_to_catalog, get_all_books
from database import update_book_availability

# -----------------------------
# Helper to generate unique ISBNs
# -----------------------------
def unique_isbn():
    import random
    return str(random.randint(1000000000000, 9999999999999))

# -----------------------------
# Test Cases for R2
# -----------------------------

def test_empty_catalog():
    """Empty catalog should return a list (possibly empty)"""
    books = get_all_books()
    assert isinstance(books, list)

def test_add_single_book_display():
    """Add a single book and verify it appears with correct fields"""
    isbn = unique_isbn()
    success, _ = add_book_to_catalog("Book One", "Author A", isbn, 3)
    assert success is True

    books = get_all_books()
    book = next(b for b in books if b["isbn"] == isbn)
    assert book["title"] == "Book One"
    assert book["author"] == "Author A"
    assert book["total_copies"] == 3
    assert book["available_copies"] == 3
    assert "id" in book
    assert "isbn" in book

def test_add_multiple_books_display():
    """Add multiple books and check all appear in catalog"""
    isbn1 = unique_isbn()
    isbn2 = unique_isbn()
    isbn3 = unique_isbn()

    add_book_to_catalog("Book Two", "Author B", isbn1, 2)
    add_book_to_catalog("Book Three", "Author C", isbn2, 1)
    add_book_to_catalog("Book Four", "Author D", isbn3, 5)

    books = get_all_books()
    added_isbns = [isbn1, isbn2, isbn3]
    found_books = [b for b in books if b["isbn"] in added_isbns]
    assert len(found_books) == 3

def test_borrow_button_logic():
    """Simulate Borrow button logic based on available copies"""
    isbn1 = unique_isbn()
    isbn2 = unique_isbn()

    # Both books must have at least 1 copy initially
    add_book_to_catalog("Book Five", "Author E", isbn1, 2)
    add_book_to_catalog("Book Six", "Author F", isbn2, 1)

    # Borrow all copies of Book Six safely
    books = get_all_books()
    book2 = next(b for b in books if b["isbn"] == isbn2)
    update_book_availability(book2["id"], -book2["available_copies"])

    # Refresh books
    books = get_all_books()
    book1 = next(b for b in books if b["isbn"] == isbn1)
    book2 = next(b for b in books if b["isbn"] == isbn2)

    # Borrow button logic
    assert book1["available_copies"] > 0   # Borrow button should appear
    assert book2["available_copies"] == 0  # Borrow button should NOT appear

def test_add_book_invalid_inputs():
    """Test invalid inputs when adding a book"""
    # title missing
    success, _ = add_book_to_catalog("", "Author H", unique_isbn(), 2)
    assert success is False
    # author missing
    success, _ = add_book_to_catalog("Title H", "", unique_isbn(), 2)
    assert success is False
    # ISBN wrong length
    success, _ = add_book_to_catalog("Title I", "Author I", "123", 2)
    assert success is False
    # total_copies <= 0
    success, _ = add_book_to_catalog("Title J", "Author J", unique_isbn(), 0)
    assert success is False
