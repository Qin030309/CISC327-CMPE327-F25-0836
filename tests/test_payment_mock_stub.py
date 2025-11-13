"""
Test file for pay_late_fees() and refund_late_fee_payment() functions
using stubbing and mocking techniques.

Stubbing: Database functions (calculate_late_fee_for_book, get_book_by_id)
Mocking: Payment gateway (PaymentGateway.process_payment, refund_payment)
"""
import pytest
from unittest.mock import Mock
from services.library_service import pay_late_fees, refund_late_fee_payment, reset_globals
from services.payment_service import PaymentGateway


class TestPayLateFees:
    """Test suite for pay_late_fees() function"""
    
    def test_successful_payment(self, mocker):
        """Test successful late fee payment"""
        reset_globals()
        
        # STUB: Database functions return fake data
        mocker.patch('services.library_service.calculate_late_fee_for_book', 
                    return_value={'fee_amount': 10.50})
        mocker.patch('services.library_service.get_book_by_id', 
                    return_value={'id': 'b1', 'title': 'Test Book'})
        
        # MOCK: Payment gateway with verification
        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.process_payment.return_value = {
            'status': 'success',
            'transaction_id': 'tx123',
            'amount': 10.50
        }
        
        # Execute (patron_id must be numeric string)
        success, message = pay_late_fees('12345', 'b1', mock_gateway)
        
        # Verify mock was called correctly with keyword arguments
        mock_gateway.process_payment.assert_called_once_with(patron_id='12345', amount=10.50)
        
        # Verify result
        assert success is True
        assert 'successfully' in message
    
    def test_payment_declined_by_gateway(self, mocker):
        """Test payment declined by gateway"""
        reset_globals()
        
        # STUB: Database functions
        mocker.patch('services.library_service.calculate_late_fee_for_book', 
                    return_value={'fee_amount': 5.00})
        mocker.patch('services.library_service.get_book_by_id', 
                    return_value={'id': 'b2', 'title': 'Book 2'})
        
        # MOCK: Gateway declines payment
        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.process_payment.return_value = {
            'status': 'declined',
            'message': 'Insufficient funds'
        }
        
        # Execute
        success, message = pay_late_fees('67890', 'b2', mock_gateway)
        
        # Verify
        mock_gateway.process_payment.assert_called_once_with(patron_id='67890', amount=5.00)
        assert success is False
        assert 'declined' in message.lower()
    
    def test_invalid_patron_id(self, mocker):
        """Test invalid patron ID - mock should NOT be called"""
        reset_globals()
        
        # STUB: Return data (won't be reached)
        mocker.patch('services.library_service.calculate_late_fee_for_book', 
                    return_value={'fee_amount': 5.00})
        mocker.patch('services.library_service.get_book_by_id', 
                    return_value={'id': 'b3', 'title': 'Book 3'})
        
        # MOCK: Gateway should not be called
        mock_gateway = Mock(spec=PaymentGateway)
        
        # Execute with invalid patron_id (not numeric)
        success, message = pay_late_fees('invalid_patron', 'b3', mock_gateway)
        
        # Verify mock NOT called
        mock_gateway.process_payment.assert_not_called()
        assert success is False
        assert 'Invalid patron ID' in message
    
    def test_invalid_patron_id_empty(self, mocker):
        """Test empty patron ID - mock should NOT be called"""
        reset_globals()
        
        # MOCK: Gateway should not be called
        mock_gateway = Mock(spec=PaymentGateway)
        
        # Execute with empty patron_id
        success, message = pay_late_fees('', 'b4', mock_gateway)
        
        # Verify mock NOT called
        mock_gateway.process_payment.assert_not_called()
        assert success is False
        assert 'Invalid patron ID' in message
    
    def test_zero_late_fees(self, mocker):
        """Test zero late fees - mock should NOT be called"""
        reset_globals()
        
        # STUB: Return zero fee
        mocker.patch('services.library_service.calculate_late_fee_for_book', 
                    return_value={'fee_amount': 0.0})
        mocker.patch('services.library_service.get_book_by_id', 
                    return_value={'id': 'b4', 'title': 'Book 4'})
        
        # MOCK: Gateway should not be called
        mock_gateway = Mock(spec=PaymentGateway)
        
        # Execute
        success, message = pay_late_fees('11111', 'b4', mock_gateway)
        
        # Verify mock NOT called
        mock_gateway.process_payment.assert_not_called()
        assert success is True
        assert 'No late fee' in message
    
    def test_network_error_exception(self, mocker):
        """Test exception handling for network errors"""
        reset_globals()
        
        # STUB: Database functions
        mocker.patch('services.library_service.calculate_late_fee_for_book', 
                    return_value={'fee_amount': 15.00})
        mocker.patch('services.library_service.get_book_by_id', 
                    return_value={'id': 'b5', 'title': 'Book 5'})
        
        # MOCK: Gateway raises exception
        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.process_payment.side_effect = Exception('Network timeout')
        
        # Execute
        success, message = pay_late_fees('22222', 'b5', mock_gateway)
        
        # Verify
        mock_gateway.process_payment.assert_called_once()
        assert success is False
        assert 'Network' in message
    
    def test_invalid_book_id(self, mocker):
        """Test with invalid book ID"""
        reset_globals()
        
        # STUB: Return None for invalid book
        mocker.patch('services.library_service.calculate_late_fee_for_book', 
                    return_value={'fee_amount': 5.00})
        mocker.patch('services.library_service.get_book_by_id', 
                    return_value=None)
        
        # MOCK
        mock_gateway = Mock(spec=PaymentGateway)
        
        # Execute
        success, message = pay_late_fees('33333', 'invalid_id', mock_gateway)
        
        # Verify mock NOT called for invalid book
        mock_gateway.process_payment.assert_not_called()
        assert success is False
        assert 'not found' in message.lower()


class TestRefundLateFeePayment:
    """Test suite for refund_late_fee_payment() function"""
    
    def test_successful_refund(self):
        """Test successful refund"""
        reset_globals()
        
        # MOCK: Gateway with successful refund
        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.refund_payment.return_value = {
            'status': 'success',
            'refund_id': 'refund_123',
            'amount': 8.50
        }
        
        # Execute
        success, message = refund_late_fee_payment('tx999', 8.50, mock_gateway)
        
        # Verify mock called with correct parameters
        mock_gateway.refund_payment.assert_called_once_with('tx999', 8.50)
        assert success is True
        assert 'successfully' in message.lower()
    
    def test_invalid_transaction_id(self):
        """Test refund with invalid transaction ID (empty)"""
        reset_globals()
        
        # MOCK: Should not be called
        mock_gateway = Mock(spec=PaymentGateway)
        
        # Execute with empty transaction_id
        success, message = refund_late_fee_payment('', 5.00, mock_gateway)
        
        # Verify mock NOT called
        mock_gateway.refund_payment.assert_not_called()
        assert success is False
        assert 'Invalid transaction ID' in message
    
    def test_negative_refund_amount(self):
        """Test refund with negative amount - should be rejected"""
        reset_globals()
        
        # MOCK: Should not be called for negative amount
        mock_gateway = Mock(spec=PaymentGateway)
        
        # Execute
        success, message = refund_late_fee_payment('tx100', -5.00, mock_gateway)
        
        # Verify mock NOT called
        mock_gateway.refund_payment.assert_not_called()
        assert success is False
        assert 'Invalid amount' in message
    
    def test_zero_refund_amount(self):
        """Test refund with zero amount - should be rejected"""
        reset_globals()
        
        # MOCK: Should not be called for zero amount
        mock_gateway = Mock(spec=PaymentGateway)
        
        # Execute
        success, message = refund_late_fee_payment('tx101', 0.0, mock_gateway)
        
        # Verify mock NOT called
        mock_gateway.refund_payment.assert_not_called()
        assert success is False
        assert 'Invalid amount' in message
    
    def test_refund_exceeds_maximum(self):
        """Test refund exceeding $15 maximum"""
        reset_globals()
        
        # MOCK: Should not be called for amount > $15
        mock_gateway = Mock(spec=PaymentGateway)
        
        # Execute
        success, message = refund_late_fee_payment('tx102', 20.00, mock_gateway)
        
        # Verify mock NOT called
        mock_gateway.refund_payment.assert_not_called()
        assert success is False
        assert 'Invalid amount' in message
    
    def test_refund_at_maximum_boundary(self):
        """Test refund at exactly $15 - should succeed"""
        reset_globals()
        
        # MOCK: Gateway accepts $15 refund
        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.refund_payment.return_value = {
            'status': 'success',
            'refund_id': 'refund_max',
            'amount': 15.00
        }
        
        # Execute
        success, message = refund_late_fee_payment('tx103', 15.00, mock_gateway)
        
        # Verify
        mock_gateway.refund_payment.assert_called_once_with('tx103', 15.00)
        assert success is True
    
    def test_refund_declined_by_gateway(self):
        """Test refund declined by gateway"""
        reset_globals()
        
        # MOCK: Gateway declines with reason
        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.refund_payment.return_value = {
            'status': 'error',
            'reason': 'Transaction not found'
        }
        
        # Execute
        success, message = refund_late_fee_payment('tx_invalid', 5.00, mock_gateway)
        
        # Verify
        mock_gateway.refund_payment.assert_called_once_with('tx_invalid', 5.00)
        assert success is False
        assert 'Transaction not found' in message
    
    def test_refund_exception_handling(self):
        """Test exception handling during refund"""
        reset_globals()
        
        # MOCK: Gateway raises exception
        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.refund_payment.side_effect = Exception('Connection error')
        
        # Execute
        success, message = refund_late_fee_payment('tx104', 10.00, mock_gateway)
        
        # Verify
        mock_gateway.refund_payment.assert_called_once()
        assert success is False
        assert 'Refund error' in message
    
    def test_refund_amount_boundary_low(self):
        """Test refund with minimum valid amount (0.01)"""
        reset_globals()
        
        # MOCK
        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.refund_payment.return_value = {'status': 'success'}
        
        # Execute
        success, message = refund_late_fee_payment('tx105', 0.01, mock_gateway)
        
        # Verify
        mock_gateway.refund_payment.assert_called_once_with('tx105', 0.01)
        assert success is True
