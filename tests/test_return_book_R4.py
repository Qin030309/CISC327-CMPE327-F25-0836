import pytest
from library_service import return_book_by_patron, borrow_book_by_patron, add_book_to_catalog
from database import init_database, add_sample_data

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Initialize database and add sample books and borrowed book for testing."""
    init_database()
    add_sample_data()
    # Add a test book for return
    add_book_to_catalog("Test Return Book", "Author R", "9999999999999", 2)
    # Borrow the book for positive test
    borrow_book_by_patron("654321", 4)

def test_return_book_not_implemented():
    """Test that R4 returns not implemented message."""
    success, message = return_book_by_patron("654321", 4)
    assert not success
    assert "not yet implemented" in message.lower()

@pytest.mark.skip(reason="R4 not implemented yet")
def test_return_book_valid_positive():
    """Positive test: returning a valid borrowed book."""
    success, message = return_book_by_patron("654321", 4)
    assert success
    assert "successfully returned" in message.lower()

@pytest.mark.skip(reason="R4 not implemented yet")
def test_return_book_not_borrowed_negative():
    """Negative test: book not borrowed by this patron."""
    success, message = return_book_by_patron("654321", 1)  # book 1 is borrowed by someone else
    assert not success
    assert "not borrowed" in message.lower()

@pytest.mark.skip(reason="R4 not implemented yet")
def test_return_book_invalid_patron_id_negative():
    """Negative test: invalid patron ID format."""
    success, message = return_book_by_patron("abc123", 4)
    assert not success
    assert "invalid patron id" in message.lower()

@pytest.mark.skip(reason="R4 not implemented yet")
def test_return_book_invalid_book_id_negative():
    """Negative test: invalid book ID."""
    success, message = return_book_by_patron("654321", 9999)
    assert not success
    assert "book not found" in message.lower()
