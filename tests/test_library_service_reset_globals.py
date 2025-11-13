from services import library_service as ls

def test_reset_globals_minimal_direct_call():
    # 直接调用函数，不用 fixture
    ls.reset_globals()
