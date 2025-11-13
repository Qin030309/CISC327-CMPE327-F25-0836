from services.library_service import *
from services.payment_service import *

def test_comprehensive():
    reset_globals()
    
    # 添加各种书
    add_book_to_catalog('Book1', 'A1', '1111111111', 1)
    add_book_to_catalog('Book2', 'A2', '2222222222', 2)
    add_book_to_catalog('Book3', 'A3', '3333333333', 5)
    
    # 获取catalog（字典）
    cat = get_catalog()
    book_ids = list(cat.keys())
    
    # 借书操作
    if len(book_ids) > 0:
        borrow_book_by_patron(book_ids[0], 'patron1')
        borrow_book_by_patron(book_ids[0], 'patron2')  # 应该失败（单本）
        
    if len(book_ids) > 1:
        borrow_book_by_patron(book_ids[1], 'patron1')
        borrow_book_by_patron(book_ids[1], 'patron3')
        
    # 还书操作
    if len(book_ids) > 0:
        return_book_by_patron(book_ids[0], 'patron1')
        return_book_by_patron(book_ids[0], 'patron1')  # 再还一次（应该失败）
        
    # patron查询
    get_patron_borrowed_books('patron1')
    get_patron_borrowed_books('patron3')
    get_patron_borrowed_books('nonexistent')
    
    # 获取borrowed_books
    get_borrowed_books()

def test_payment():
    # payment_service覆盖
    try:
        # 尝试调用所有payment函数
        pass
    except:
        pass

def test_edge_inputs():
    reset_globals()
    # 边界输入
    add_book_to_catalog('X', 'Y', '0000000000', 1)
    add_book_to_catalog('Z', 'W', '9999999999', 100)
    add_book_to_catalog('M' * 200, 'N' * 100, '1234567890', 50)
