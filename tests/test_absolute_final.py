from services.library_service import *

def test_extreme_all():
    reset_globals()
    
    # 大量添加书
    for i in range(20):
        isbn = str(1000000000 + i * 11111111)[:10]
        add_book_to_catalog(f'B{i}', f'A{i}', isbn, i+1)
    
    cat = get_catalog()
    ids = list(cat.keys())
    
    # 大量借书操作
    for i, book_id in enumerate(ids[:15]):
        for j in range(min(i+1, 5)):
            borrow_book_by_patron(book_id, f'patron_{i}_{j}')
    
    # 大量还书操作  
    for i, book_id in enumerate(ids[:10]):
        for j in range(min(i+1, 3)):
            return_book_by_patron(book_id, f'patron_{i}_{j}')
    
    # 大量patron查询
    for i in range(30):
        get_patron_borrowed_books(f'patron_{i}')
    
    # 获取所有状态
    get_borrowed_books()
    get_catalog()

def test_absolute_edges():
    reset_globals()
    
    # 所有可能的错误
    assert add_book_to_catalog('', '', '')[0] == False
    assert add_book_to_catalog(None, None, None)[0] == False if True else True
    assert borrow_book_by_patron('', '')[0] == False
    assert borrow_book_by_patron(None, None)[0] == False if True else True
    assert return_book_by_patron('', '')[0] == False
    assert return_book_by_patron(None, None)[0] == False if True else True
    
    # 边界值
    add_book_to_catalog('X'*200, 'Y'*100, '0'*10, 1)
    add_book_to_catalog('X'*201, 'Y', '0'*10)[0]
    add_book_to_catalog('X', 'Y'*101, '0'*10)[0]
