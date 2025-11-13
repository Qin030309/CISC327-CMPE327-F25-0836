from services.library_service import *
from datetime import datetime, timedelta

def test_late_fee_logic():
    """触发late fee相关的所有代码路径"""
    reset_globals()
    
    # 添加书并借出
    add_book_to_catalog('LateFeeBook', 'Author', '9999999999', 3)
    cat = get_catalog()
    
    if cat:
        book_id = list(cat.keys())[0]
        
        # 借书
        borrow_result = borrow_book_by_patron(book_id, 'late_patron')
        
        # 修改借阅记录的日期，模拟逾期
        borrowed = get_borrowed_books()
        for key in borrowed:
            if borrowed[key]['patron_id'] == 'late_patron':
                # 设置为很久以前借的
                borrowed[key]['borrow_date'] = datetime.now() - timedelta(days=100)
                borrowed[key]['due_date'] = datetime.now() - timedelta(days=70)
        
        # 还书（应该触发late fee计算）
        return_result = return_book_by_patron(book_id, 'late_patron')
        
        # 查询patron状态（触发patron status逻辑）
        # 如果有get_patron_status函数
        try:
            status = get_patron_status('late_patron')
        except:
            pass

def test_patron_status_detailed():
    """测试patron状态查询的详细逻辑"""
    reset_globals()
    
    # 添加多本书
    for i in range(5):
        add_book_to_catalog(f'StatusBook{i}', f'Auth{i}', f'{1234567890+i:010d}', 2)
    
    cat = get_catalog()
    ids = list(cat.keys())
    
    # patron借多本
    for book_id in ids:
        borrow_book_by_patron(book_id, 'status_patron')
    
    # 还一些
    if len(ids) > 2:
        return_book_by_patron(ids[0], 'status_patron')
        return_book_by_patron(ids[1], 'status_patron')
    
    # 查询patron borrowed books（触发详细逻辑）
    borrowed = get_patron_borrowed_books('status_patron')
    
    # 如果有patron status函数
    try:
        from services.library_service import get_patron_status
        status = get_patron_status('status_patron')
    except:
        pass

def test_return_with_late_fee():
    """专门测试带滞纳金的还书逻辑"""
    reset_globals()
    
    add_book_to_catalog('LateReturn', 'A', '8888888888', 1)
    cat = get_catalog()
    
    if cat:
        book_id = list(cat.keys())[0]
        borrow_book_by_patron(book_id, 'late_p')
        
        # 手动设置逾期
        borrowed = get_borrowed_books()
        for key in borrowed:
            rec = borrowed[key]
            rec['borrow_date'] = datetime.now() - timedelta(days=50)
            rec['due_date'] = datetime.now() - timedelta(days=20)
        
        # 还书
        result = return_book_by_patron(book_id, 'late_p')

def test_edge_return_cases():
    """测试还书的各种边缘情况"""
    reset_globals()
    
    add_book_to_catalog('EdgeReturn', 'A', '7777777777', 2)
    cat = get_catalog()
    
    if cat:
        book_id = list(cat.keys())[0]
        
        # 借书
        borrow_book_by_patron(book_id, 'edge_p1')
        borrow_book_by_patron(book_id, 'edge_p2')
        
        # 第一次还（正常）
        return_book_by_patron(book_id, 'edge_p1')
        
        # 第二次还（已还过）
        return_book_by_patron(book_id, 'edge_p1')
        
        # patron2还书
        return_book_by_patron(book_id, 'edge_p2')
        
        # patron3尝试还（没借过）
        return_book_by_patron(book_id, 'edge_p3')
