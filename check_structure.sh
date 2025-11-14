#!/bin/bash

echo "==== 步骤 1: 检查 services 文件夹 ===="
if [ -d "services" ]; then
    echo "✅ services/ 文件夹存在"
else
    echo "❌ services/ 文件夹不存在"
    exit 1
fi

echo "==== 检查 services/library_service.py ===="
if [ -f "services/library_service.py" ]; then
    echo "✅ library_service.py 存在"
else
    echo "❌ library_service.py 不存在"
    exit 1
fi

echo "==== 检查 services/payment_service.py ===="
if [ -f "services/payment_service.py" ]; then
    echo "✅ payment_service.py 存在"
else
    echo "❌ payment_service.py 不存在"
    exit 1
fi

echo "==== 检查 tests 文件夹 ===="
if [ -d "tests" ]; then
    echo "✅ tests/ 文件夹存在"
else
    echo "❌ tests/ 文件夹不存在"
    exit 1
fi

echo "==== 检查 test_library_service_payment.py ===="
if [ -f "tests/test_library_service_payment.py" ]; then
    echo "✅ test_library_service_payment.py 存在"
else
    echo "❌ test_library_service_payment.py 不存在"
    exit 1
fi

echo "==== 检查 library_service.py 内函数 ===="
grep -q "def pay_late_fees" services/library_service.py
if [ $? -eq 0 ]; then
    echo "✅ pay_late_fees() 存在"
else
    echo "❌ pay_late_fees() 不存在"
fi

grep -q "def refund_late_fee_payment" services/library_service.py
if [ $? -eq 0 ]; then
    echo "✅ refund_late_fee_payment() 存在"
else
    echo "❌ refund_late_fee_payment() 不存在"
fi

echo "==== 检查 payment_service.py 内 PaymentGateway 类 ===="
grep -q "class PaymentGateway" services/payment_service.py
if [ $? -eq 0 ]; then
    echo "✅ PaymentGateway 类存在"
else
    echo "❌ PaymentGateway 类不存在"
fi

echo "==== 尝试运行 pytest 导入检查 ===="
pytest --maxfail=1 --disable-warnings -q tests/
if [ $? -eq 0 ]; then
    echo "✅ pytest 测试可以运行，导入正确"
else
    echo "❌ pytest 导入错误，请检查 import 路径"
fi

echo "==== 步骤 1 完成 ===="
