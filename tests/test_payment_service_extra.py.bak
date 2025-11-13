from unittest.mock import Mock
import pytest
from services.payment_service import PaymentGateway

def test_process_payment_failed_branch():
    gateway = PaymentGateway()
    # 模拟支付失败
    gateway.process_payment = Mock(return_value={"status": "failed"})
    result = gateway.process_payment("patronX", 50.0)
    assert result["status"] == "failed"
    gateway.process_payment.assert_called_once_with("patronX", 50.0)

def test_refund_payment_partial_branch():
    gateway = PaymentGateway()
    # 模拟退款异常
    def raise_exception(tx_id, amount):
        raise Exception("Network issue")
    gateway.refund_payment = Mock(side_effect=raise_exception)
    with pytest.raises(Exception) as exc:
        gateway.refund_payment("tx999", 10.0)
    assert str(exc.value) == "Network issue"
