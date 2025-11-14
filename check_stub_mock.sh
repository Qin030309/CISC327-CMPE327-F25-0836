#!/bin/bash

echo "==== 检查 Stubbing 和 Mocking ===="

FILE="tests/test_library_service_payment.py"

# 检查 Stub 是否存在
grep -q "@patch(\"services.library_service.calculate_late_fee_for_book\")" $FILE
if [ $? -eq 0 ]; then
    echo "✅ calculate_late_fee_for_book stub 存在"
else
    echo "❌ calculate_late_fee_for_book stub 缺失"
fi

grep -q "@patch(\"services.library_service.get_book_by_id\")" $FILE
if [ $? -eq 0 ]; then
    echo "✅ get_book_by_id stub 存在"
else
    echo "❌ get_book_by_id stub 缺失"
fi

# 检查 Mock 是否存在
grep -q "mock_gateway = Mock()" $FILE
if [ $? -eq 0 ]; then
    echo "✅ PaymentGateway mock 存在"
else
    echo "❌ PaymentGateway mock 缺失"
fi

# 检查 assert_called_once()
grep -q "assert_called_once" $FILE
if [ $? -eq 0 ]; then
    echo "✅ assert_called_once() 使用正确"
else
    echo "❌ assert_called_once() 缺失"
fi

# 检查 assert_called_with()
grep -q "assert_called_with" $FILE
if [ $? -eq 0 ]; then
    echo "✅ assert_called_with() 使用正确"
else
    echo "❌ assert_called_with() 缺失"
fi

# 检查 assert_not_called()
grep -q "assert_not_called" $FILE
if [ $? -eq 0 ]; then
    echo "✅ assert_not_called() 使用正确"
else
    echo "❌ assert_not_called() 缺失"
fi

echo "==== 检查完成 ===="
