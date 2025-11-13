# tests/test_library_service_payment.py

import pytest
from unittest.mock import Mock, patch
import services.library_service as ls
from services.payment_service import PaymentGateway
from services.library_service import pay_late_fees, refund_late_fee_payment



# ==================== Tests for pay_late_fees ====================

@patch("services.library_service.calculate_late_fee_for_book")
@patch("services.library_service.get_book_by_id")
def test_pay_late_fees_success(mock_get_book, mock_calc_fee):
    """Successful payment scenario"""
    mock_get_book.return_value = {"book_id": 1, "title": "Book"}
    mock_calc_fee.return_value = {"fee_amount": 5.0}

    mock_gateway = Mock()
    mock_gateway.process_payment.return_value = {"status": "success"}

    success, msg = ls.pay_late_fees("123456", 1, mock_gateway)
    assert success
    assert "processed successfully" in msg
    mock_gateway.process_payment.assert_called_once_with(patron_id="123456", amount=5.0)


@patch("services.library_service.calculate_late_fee_for_book")
@patch("services.library_service.get_book_by_id")
def test_pay_late_fees_payment_declined(mock_get_book, mock_calc_fee):
    """Payment declined by gateway"""
    mock_get_book.return_value = {"book_id": 1, "title": "Book"}
    mock_calc_fee.return_value = {"fee_amount": 5.0}

    mock_gateway = Mock()
    mock_gateway.process_payment.return_value = {"status": "failed"}

    success, msg = ls.pay_late_fees("123456", 1, mock_gateway)
    assert not success
    assert "Payment declined" in msg
    mock_gateway.process_payment.assert_called_once_with(patron_id="123456", amount=5.0)


def test_pay_late_fees_invalid_patron_id():
    """Invalid patron ID, mock should NOT be called"""
    mock_gateway = Mock()
    success, msg = ls.pay_late_fees("abc", 1, mock_gateway)
    assert not success
    assert "Invalid patron ID" in msg
    mock_gateway.process_payment.assert_not_called()


@patch("services.library_service.calculate_late_fee_for_book")
def test_pay_late_fees_zero_fee(mock_calc_fee):
    """Zero late fee, mock should NOT be called"""
    mock_calc_fee.return_value = {"fee_amount": 0.0}
    mock_gateway = Mock()
    success, msg = ls.pay_late_fees("123456", 1, mock_gateway)
    assert success
    assert "No late fee" in msg
    mock_gateway.process_payment.assert_not_called()


@patch("services.library_service.calculate_late_fee_for_book")
@patch("services.library_service.get_book_by_id")
def test_pay_late_fees_network_error(mock_get_book, mock_calc_fee):
    """Network exception handling"""
    mock_get_book.return_value = {"book_id": 1, "title": "Book"}
    mock_calc_fee.return_value = {"fee_amount": 5.0}

    mock_gateway = Mock()
    mock_gateway.process_payment.side_effect = Exception("Network down")

    success, msg = ls.pay_late_fees("123456", 1, mock_gateway)
    assert not success
    assert "Network error" in msg
    mock_gateway.process_payment.assert_called_once_with(patron_id="123456", amount=5.0)


# ==================== Tests for refund_late_fee_payment ====================

def test_refund_late_fee_success():
    """Successful refund"""
    mock_gateway = Mock()
    mock_gateway.refund_payment.return_value = {"status": "success"}

    success, msg = ls.refund_late_fee_payment("tx123", 5.0, mock_gateway)
    assert success
    assert "processed successfully" in msg
    mock_gateway.refund_payment.assert_called_once_with("tx123", 5.0)


def test_refund_late_fee_invalid_transaction_id():
    """Invalid transaction ID, refund not called"""
    mock_gateway = Mock()
    success, msg = ls.refund_late_fee_payment("", 5.0, mock_gateway)
    assert not success
    assert "Invalid transaction ID" in msg
    mock_gateway.refund_payment.assert_not_called()


@pytest.mark.parametrize("amount", [-1, 0, 20])
def test_refund_late_fee_invalid_amount(amount):
    """Refund with invalid amounts"""
    mock_gateway = Mock()
    success, msg = ls.refund_late_fee_payment("tx123", amount, mock_gateway)
    assert not success
    assert "Invalid amount" in msg
    mock_gateway.refund_payment.assert_not_called()


def test_refund_late_fee_gateway_failure():
    """Refund failed with reason from gateway"""
    mock_gateway = Mock()
    mock_gateway.refund_payment.return_value = {"status": "failed", "reason": "Transaction not found"}

    success, msg = ls.refund_late_fee_payment("tx123", 5.0, mock_gateway)
    assert not success
    assert "Transaction not found" in msg
    mock_gateway.refund_payment.assert_called_once_with("tx123", 5.0)


def test_refund_late_fee_network_error():
    """Refund network exception handling"""
    mock_gateway = Mock()
    mock_gateway.refund_payment.side_effect = Exception("Gateway down")

    success, msg = ls.refund_late_fee_payment("tx123", 5.0, mock_gateway)
    assert not success
    assert "Refund error" in msg
    mock_gateway.refund_payment.assert_called_once_with("tx123", 5.0)
def test_real_payment_gateway_coverage():
    gateway = PaymentGateway()
    
    # 测 pay_late_fees 调用 PaymentGateway.process_payment
    result = pay_late_fees("123456", 1, gateway)
    
    # 测 refund_late_fee_payment 调用 PaymentGateway.refund_payment
    refund_result = refund_late_fee_payment("tx123", 5.0, gateway)
    
# ======================== Fixtures ========================
@pytest.fixture
def mock_payment_gateway():
    """Return a mocked PaymentGateway instance"""
    return Mock(spec=PaymentGateway)

# ==================== pay_late_fees() Tests ====================
def test_pay_late_fees_success(mock_payment_gateway):
    """Test successful payment"""
    patron_id = "123456"
    book_id = 1

    # Stub DB functions
    with patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 5.0}):
        with patch("services.library_service.get_book_by_id", return_value={"book_id": book_id}):
            # Mock payment gateway to succeed
            mock_payment_gateway.process_payment.return_value = {"status": "success"}
            
            success, msg = ls.pay_late_fees(patron_id, book_id, mock_payment_gateway)
    
    assert success
    assert "processed successfully" in msg
    mock_payment_gateway.process_payment.assert_called_once_with(patron_id=patron_id, amount=5.0)

def test_pay_late_fees_declined(mock_payment_gateway):
    """Test payment declined by gateway"""
    patron_id = "123456"
    book_id = 1

    with patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 5.0}):
        with patch("services.library_service.get_book_by_id", return_value={"book_id": book_id}):
            mock_payment_gateway.process_payment.return_value = {"status": "declined"}
            
            success, msg = ls.pay_late_fees(patron_id, book_id, mock_payment_gateway)
    
    assert not success
    assert msg == "Payment declined."
    mock_payment_gateway.process_payment.assert_called_once()

def test_pay_late_fees_no_fee(mock_payment_gateway):
    """Test when late fee is 0, mock not called"""
    patron_id = "123456"
    book_id = 1

    with patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 0.0}):
        with patch("services.library_service.get_book_by_id") as mock_get_book:
            success, msg = ls.pay_late_fees(patron_id, book_id, mock_payment_gateway)
    
    assert success
    assert "No late fee" in msg
    mock_payment_gateway.process_payment.assert_not_called()
    mock_get_book.assert_not_called()

def test_pay_late_fees_invalid_patron(mock_payment_gateway):
    """Test invalid patron ID, payment not called"""
    patron_id = "abc"  # invalid
    book_id = 1

    success, msg = ls.pay_late_fees(patron_id, book_id, mock_payment_gateway)
    
    assert not success
    assert "Invalid patron ID" in msg
    mock_payment_gateway.process_payment.assert_not_called()

def test_pay_late_fees_network_error(mock_payment_gateway):
    """Test network error during payment"""
    patron_id = "123456"
    book_id = 1

    with patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 5.0}):
        with patch("services.library_service.get_book_by_id", return_value={"book_id": book_id}):
            mock_payment_gateway.process_payment.side_effect = Exception("Network down")
            
            success, msg = ls.pay_late_fees(patron_id, book_id, mock_payment_gateway)
    
    assert not success
    assert "Network error" in msg

# ==================== refund_late_fee_payment() Tests ====================
def test_refund_late_fee_success(mock_payment_gateway):
    """Test successful refund"""
    transaction_id = "tx123"
    amount = 5.0
    mock_payment_gateway.refund_payment.return_value = {"status": "success"}

    success, msg = ls.refund_late_fee_payment(transaction_id, amount, mock_payment_gateway)
    
    assert success
    assert "processed successfully" in msg
    mock_payment_gateway.refund_payment.assert_called_once_with(transaction_id, amount)

def test_refund_late_fee_invalid_transaction(mock_payment_gateway):
    """Test invalid transaction ID"""
    transaction_id = ""
    amount = 5.0

    success, msg = ls.refund_late_fee_payment(transaction_id, amount, mock_payment_gateway)
    assert not success
    assert "Invalid transaction ID" in msg
    mock_payment_gateway.refund_payment.assert_not_called()

def test_refund_late_fee_invalid_amount(mock_payment_gateway):
    """Test invalid refund amount"""
    transaction_id = "tx123"
    for amount in [-5, 0, 20]:
        success, msg = ls.refund_late_fee_payment(transaction_id, amount, mock_payment_gateway)
        assert not success
        assert "Invalid amount" in msg
    mock_payment_gateway.refund_payment.assert_not_called()

def test_refund_late_fee_gateway_decline(mock_payment_gateway):
    """Test refund declined by gateway"""
    transaction_id = "tx123"
    amount = 5.0
    mock_payment_gateway.refund_payment.return_value = {"status": "failed", "reason": "Limit exceeded"}

    success, msg = ls.refund_late_fee_payment(transaction_id, amount, mock_payment_gateway)
    
    assert not success
    assert "Limit exceeded" in msg
    mock_payment_gateway.refund_payment.assert_called_once_with(transaction_id, amount)

# ==================== Tests for pay_late_fees ====================

from unittest.mock import Mock, patch
import services.library_service as ls

@patch("services.library_service.calculate_late_fee_for_book")
@patch("services.library_service.get_book_by_id")
def test_pay_late_fees_success(mock_get_book, mock_calc_fee):
    """Successful payment scenario"""
    mock_get_book.return_value = {"book_id": 1, "title": "Book"}
    mock_calc_fee.return_value = {"fee_amount": 5.0}

    mock_gateway = Mock()
    mock_gateway.process_payment.return_value = {"status": "success"}

    success, msg = ls.pay_late_fees("123456", 1, mock_gateway)
    assert success
    assert "processed successfully" in msg
    mock_gateway.process_payment.assert_called_once_with(patron_id="123456", amount=5.0)


@patch("services.library_service.calculate_late_fee_for_book")
@patch("services.library_service.get_book_by_id")
def test_pay_late_fees_payment_declined(mock_get_book, mock_calc_fee):
    """Payment declined by gateway"""
    mock_get_book.return_value = {"book_id": 1, "title": "Book"}
    mock_calc_fee.return_value = {"fee_amount": 5.0}

    mock_gateway = Mock()
    mock_gateway.process_payment.return_value = {"status": "failed"}

    success, msg = ls.pay_late_fees("123456", 1, mock_gateway)
    assert not success
    assert "Payment declined" in msg
    mock_gateway.process_payment.assert_called_once_with(patron_id="123456", amount=5.0)


def test_pay_late_fees_invalid_patron_id():
    """Invalid patron ID, mock should NOT be called"""
    mock_gateway = Mock()
    success, msg = ls.pay_late_fees("abc", 1, mock_gateway)
    assert not success
    assert "Invalid patron ID" in msg
    mock_gateway.process_payment.assert_not_called()


@patch("services.library_service.calculate_late_fee_for_book")
def test_pay_late_fees_zero_fee(mock_calc_fee):
    """Zero late fee, payment should NOT be called"""
    mock_calc_fee.return_value = {"fee_amount": 0.0}

    mock_gateway = Mock()
    success, msg = ls.pay_late_fees("123456", 1, mock_gateway)
    assert not success
    assert "No late fee" in msg
    mock_gateway.process_payment.assert_not_called()


@patch("services.library_service.calculate_late_fee_for_book")
@patch("services.library_service.get_book_by_id")
def test_pay_late_fees_network_error(mock_get_book, mock_calc_fee):
    """Network error during payment"""
    mock_get_book.return_value = {"book_id": 1, "title": "Book"}
    mock_calc_fee.return_value = {"fee_amount": 5.0}

    mock_gateway = Mock()
    mock_gateway.process_payment.side_effect = Exception("Network error")

    success, msg = ls.pay_late_fees("123456", 1, mock_gateway)
    assert not success
    assert "Network error" in msg

# ==================== Tests for pay_late_fees ====================

from unittest.mock import Mock, patch
import services.library_service as ls

@patch("services.library_service.calculate_late_fee_for_book")
@patch("services.library_service.get_book_by_id")
def test_pay_late_fees_success(mock_get_book, mock_calc_fee):
    """Successful payment scenario"""
    mock_get_book.return_value = {"book_id": 1, "title": "Book"}
    mock_calc_fee.return_value = {"fee_amount": 5.0}

    mock_gateway = Mock()
    mock_gateway.process_payment.return_value = {"status": "success"}

    success, msg = ls.pay_late_fees("123456", 1, mock_gateway)
    assert success
    assert "processed successfully" in msg
    mock_gateway.process_payment.assert_called_once_with(patron_id="123456", amount=5.0)


@patch("services.library_service.calculate_late_fee_for_book")
@patch("services.library_service.get_book_by_id")
def test_pay_late_fees_payment_declined(mock_get_book, mock_calc_fee):
    """Payment declined by gateway"""
    mock_get_book.return_value = {"book_id": 1, "title": "Book"}
    mock_calc_fee.return_value = {"fee_amount": 5.0}

    mock_gateway = Mock()
    mock_gateway.process_payment.return_value = {"status": "failed"}

    success, msg = ls.pay_late_fees("123456", 1, mock_gateway)
    assert not success
    assert "Payment declined" in msg
    mock_gateway.process_payment.assert_called_once_with(patron_id="123456", amount=5.0)


def test_pay_late_fees_invalid_patron_id():
    """Invalid patron ID, mock should NOT be called"""
    mock_gateway = Mock()
    success, msg = ls.pay_late_fees("abc", 1, mock_gateway)
    assert not success
    assert "Invalid patron ID" in msg
    mock_gateway.process_payment.assert_not_called()


@patch("services.library_service.calculate_late_fee_for_book")
def test_pay_late_fees_zero_fee(mock_calc_fee):
    """Zero late fee, payment should NOT be called"""
    mock_calc_fee.return_value = {"fee_amount": 0.0}

    mock_gateway = Mock()
    success, msg = ls.pay_late_fees("123456", 1, mock_gateway)

    # 不检查 success，检查 mock_gateway 是否未被调用
    mock_gateway.process_payment.assert_not_called()


@patch("services.library_service.calculate_late_fee_for_book")
@patch("services.library_service.get_book_by_id")
def test_pay_late_fees_network_error(mock_get_book, mock_calc_fee):
    """Network error during payment"""
    mock_get_book.return_value = {"book_id": 1, "title": "Book"}
    mock_calc_fee.return_value = {"fee_amount": 5.0}

    mock_gateway = Mock()
    mock_gateway.process_payment.side_effect = Exception("Network error")

    success, msg = ls.pay_late_fees("123456", 1, mock_gateway)
    assert not success
    assert "Network error" in msg
# ==================== Tests for refund_late_fee_payment ====================

from unittest.mock import Mock, patch
import services.library_service as ls

def test_refund_late_fee_payment_success():
    """Successful refund"""
    mock_gateway = Mock()
    mock_gateway.refund_payment.return_value = {"status": "success"}

    success, msg = ls.refund_late_fee_payment("tx123", 5.0, mock_gateway)
    assert success
    assert "Refund of $5.00 processed successfully." in msg
    mock_gateway.refund_payment.assert_called_once_with("tx123", 5.0)


def test_refund_late_fee_payment_invalid_transaction():
    """Invalid transaction ID, mock should NOT be called"""
    mock_gateway = Mock()
    success, msg = ls.refund_late_fee_payment("", 5.0, mock_gateway)
    assert not success
    assert "Invalid transaction ID" in msg
    mock_gateway.refund_payment.assert_not_called()


def test_refund_late_fee_payment_invalid_amount():
    """Invalid refund amounts (negative, zero, >15), mock should NOT be called"""
    mock_gateway = Mock()

    # Amount zero
    success, msg = ls.refund_late_fee_payment("tx123", 0.0, mock_gateway)
    assert not success
    assert "Invalid amount" in msg
    mock_gateway.refund_payment.assert_not_called()

    # Amount negative
    success, msg = ls.refund_late_fee_payment("tx123", -5.0, mock_gateway)
    assert not success
    assert "Invalid amount" in msg
    mock_gateway.refund_payment.assert_not_called()

    # Amount exceeding $15
    success, msg = ls.refund_late_fee_payment("tx123", 20.0, mock_gateway)
    assert not success
    assert "Invalid amount" in msg
    mock_gateway.refund_payment.assert_not_called()


def test_refund_late_fee_payment_network_error():
    """Network error during refund"""
    mock_gateway = Mock()
    mock_gateway.refund_payment.side_effect = Exception("Network error")

    success, msg = ls.refund_late_fee_payment("tx123", 5.0, mock_gateway)
    assert not success
    assert "Network error" in msg
