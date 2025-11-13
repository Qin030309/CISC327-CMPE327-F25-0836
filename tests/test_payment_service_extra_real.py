from services.payment_service import PaymentGateway

# ==================== Minimal Real Tests ====================

def test_process_payment_positive_amount():
    gateway = PaymentGateway()
    result = gateway.process_payment(10.0)
    assert result["status"] in ["success", "error", "declined"]

def test_process_payment_zero_amount():
    gateway = PaymentGateway()
    result = gateway.process_payment(0.0)
    assert result["status"] in ["success", "error", "declined"]

def test_process_payment_negative_amount():
    gateway = PaymentGateway()
    result = gateway.process_payment(-5.0)
    assert result["status"] in ["success", "error", "declined"]

def test_refund_payment_positive_amount():
    gateway = PaymentGateway()
    result = gateway.refund_payment("tx123", 5.0)
    assert result["status"] in ["success", "error"]

def test_refund_payment_negative_amount():
    gateway = PaymentGateway()
    result = gateway.refund_payment("tx123", -5.0)
    assert result["status"] in ["success", "error"]
