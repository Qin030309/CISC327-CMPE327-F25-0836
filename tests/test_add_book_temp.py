from services.library_service import add_book_to_catalog, reset_globals

def test_add_book_to_catalog_valid():
    reset_globals()
    result = add_book_to_catalog('Test Book', 'Author A', '1234567890')
    assert result[0] == True
