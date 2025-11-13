from services.library_service import *

def test_all_validations():
    reset_globals()
    assert add_book_to_catalog('', 'A', '1234567890')[0] == False
    assert add_book_to_catalog('T', '', '1234567890')[0] == False
    assert add_book_to_catalog('T' * 201, 'A', '1234567890')[0] == False
    assert add_book_to_catalog('T', 'A' * 101, '1234567890')[0] == False
    assert add_book_to_catalog('T', 'A', '')[0] == False
    assert add_book_to_catalog('T', 'A', '123')[0] == False
    assert add_book_to_catalog('T', 'A', '12345678901')[0] == False
    assert add_book_to_catalog('T', 'A', 'abc1234567')[0] == False
    assert add_book_to_catalog('T', 'A', '1234567890', 0)[0] == False
    assert add_book_to_catalog('T', 'A', '1234567890', -1)[0] == False

def test_success_cases():
    reset_globals()
    assert add_book_to_catalog('Book1', 'Author1', '1234567890', 1)[0] == True
    assert add_book_to_catalog('Book2', 'Author2', '1234567890123', 5)[0] == True
    assert add_book_to_catalog('A' * 200, 'B' * 100, '9876543210', 10)[0] == True

def test_duplicate_isbn():
    reset_globals()
    add_book_to_catalog('First', 'A', '5555555555')
    result = add_book_to_catalog('Second', 'B', '5555555555')
    assert result[0] == False

def test_borrow_errors():
    reset_globals()
    assert borrow_book_by_patron('999', 'patron')[0] == False
    assert borrow_book_by_patron('fake', 'patron')[0] == False

def test_return_errors():
    reset_globals()
    assert return_book_by_patron('999', 'patron')[0] == False

def test_empty_patron():
    reset_globals()
    borrowed = get_patron_borrowed_books('nonexistent')
    assert isinstance(borrowed, list)

def test_whitespace():
    reset_globals()
    assert add_book_to_catalog('   ', 'A', '1234567890')[0] == False
    assert add_book_to_catalog('T', '   ', '1234567890')[0] == False

def test_many_copies():
    reset_globals()
    for i in range(1, 11):
        isbn = str(1000000000 + i * 111111111)[:10]
        add_book_to_catalog(f'Book{i}', f'Auth{i}', isbn, i)
