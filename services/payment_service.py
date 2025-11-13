"""
Payment service module for handling payments and refunds.
"""

class PaymentGateway:
    """Payment gateway for processing payments and refunds."""
    
    def __init__(self):
        self.transactions = {}
        self.transaction_counter = 0
    
    def process_payment(self, amount):
        """
        Process a payment.
        
        Args:
            amount: Payment amount
        
        Returns:
            dict: Payment result with status and transaction_id
        """
        if amount <= 0:
            return {"status": "declined", "message": "Invalid amount"}
        
        # Simulate payment processing
        self.transaction_counter += 1
        transaction_id = f"tx{self.transaction_counter}"
        
        self.transactions[transaction_id] = {
            "amount": amount,
            "status": "completed",
            "type": "payment"
        }
        
        return {
            "status": "success",
            "transaction_id": transaction_id,
            "amount": amount
        }
    
    def refund_payment(self, transaction_id, amount):
        """
        Process a refund.
        
        Args:
            transaction_id: Original transaction ID
            amount: Refund amount
        
        Returns:
            dict: Refund result
        """
        if not transaction_id or transaction_id not in self.transactions:
            return {"status": "error", "message": "Invalid transaction"}
        
        if amount <= 0:
            return {"status": "error", "message": "Invalid refund amount"}
        
        # Process refund
        refund_id = f"refund_{transaction_id}"
        self.transactions[refund_id] = {
            "amount": -amount,
            "status": "refunded",
            "type": "refund",
            "original_transaction": transaction_id
        }
        
        return {
            "status": "success",
            "refund_id": refund_id,
            "amount": amount
        }
