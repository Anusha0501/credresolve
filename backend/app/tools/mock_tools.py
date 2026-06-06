from typing import Dict, Optional
from datetime import datetime, timedelta
import random

class CRMTool:
    """Mock CRM tool for fetching customer data"""
    
    def __init__(self):
        # Mock customer database
        self.customers = {
            "+919876543210": {
                "name": "Rajesh Kumar",
                "due_amount": 45000.0,
                "loan_type": "Personal Loan",
                "risk_category": "medium",
                "overdue_days": 45
            },
            "+919123456789": {
                "name": "Priya Sharma",
                "due_amount": 75000.0,
                "loan_type": "Home Loan EMI",
                "risk_category": "high",
                "overdue_days": 90
            },
            "+919876543211": {
                "name": "Amit Singh",
                "due_amount": 25000.0,
                "loan_type": "Credit Card",
                "risk_category": "low",
                "overdue_days": 15
            }
        }
    
    def fetch_customer_data(self, phone_number: str) -> Optional[Dict]:
        """Fetch customer data by phone number"""
        return self.customers.get(phone_number)
    
    def get_customer_summary(self, phone_number: str) -> str:
        """Get formatted customer summary"""
        data = self.fetch_customer_data(phone_number)
        if not data:
            return "Customer not found"
        
        return f"""
        Customer: {data['name']}
        Due Amount: ₹{data['due_amount']:,.2f}
        Loan Type: {data['loan_type']}
        Risk Category: {data['risk_category']}
        Overdue Days: {data['overdue_days']}
        """

class TicketTool:
    """Mock ticket management tool"""
    
    def __init__(self):
        self.tickets = []
        self.ticket_id = 1000
    
    def create_ticket(self, phone_number: str, issue_type: str, description: str) -> Dict:
        """Create a new support ticket"""
        ticket = {
            "ticket_id": self.ticket_id,
            "phone_number": phone_number,
            "issue_type": issue_type,
            "description": description,
            "status": "open",
            "created_at": datetime.now().isoformat()
        }
        self.tickets.append(ticket)
        self.ticket_id += 1
        return ticket
    
    def update_ticket(self, ticket_id: int, status: str, notes: str = "") -> Optional[Dict]:
        """Update ticket status"""
        for ticket in self.tickets:
            if ticket["ticket_id"] == ticket_id:
                ticket["status"] = status
                ticket["notes"] = notes
                ticket["updated_at"] = datetime.now().isoformat()
                return ticket
        return None
    
    def get_tickets(self, phone_number: str) -> list:
        """Get all tickets for a phone number"""
        return [t for t in self.tickets if t["phone_number"] == phone_number]

class PaymentTool:
    """Mock payment calculation tool"""
    
    def calculate_outstanding(self, principal: float, interest_rate: float, overdue_days: int) -> Dict:
        """Calculate outstanding amount with interest"""
        daily_interest = (principal * interest_rate / 100) / 365
        interest_amount = daily_interest * overdue_days
        total_outstanding = principal + interest_amount
        
        return {
            "principal": principal,
            "interest_amount": interest_amount,
            "total_outstanding": total_outstanding,
            "breakdown": f"Principal: ₹{principal:,.2f}, Interest: ₹{interest_amount:,.2f}"
        }
    
    def calculate_settlement(self, outstanding_amount: float, settlement_percentage: float = 70) -> Dict:
        """Calculate settlement amount"""
        settlement_amount = outstanding_amount * (settlement_percentage / 100)
        savings = outstanding_amount - settlement_amount
        
        return {
            "original_amount": outstanding_amount,
            "settlement_percentage": settlement_percentage,
            "settlement_amount": settlement_amount,
            "savings": savings,
            "valid_until": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        }
    
    def calculate_emi_restructuring(self, outstanding_amount: float, months: int = 6) -> Dict:
        """Calculate EMI restructuring options"""
        monthly_emi = outstanding_amount / months
        processing_fee = outstanding_amount * 0.02
        
        return {
            "outstanding_amount": outstanding_amount,
            "tenure_months": months,
            "monthly_emi": monthly_emi,
            "processing_fee": processing_fee,
            "total_repayment": outstanding_amount + processing_fee
        }

class SMSTool:
    """Mock SMS sending tool"""
    
    def __init__(self):
        self.sms_log = []
    
    def send_reminder(self, phone_number: str, message: str) -> Dict:
        """Send reminder SMS"""
        sms = {
            "sms_id": len(self.sms_log) + 1,
            "phone_number": phone_number,
            "type": "reminder",
            "message": message,
            "status": "sent",
            "sent_at": datetime.now().isoformat()
        }
        self.sms_log.append(sms)
        return sms
    
    def send_confirmation(self, phone_number: str, message: str) -> Dict:
        """Send confirmation SMS"""
        sms = {
            "sms_id": len(self.sms_log) + 1,
            "phone_number": phone_number,
            "type": "confirmation",
            "message": message,
            "status": "sent",
            "sent_at": datetime.now().isoformat()
        }
        self.sms_log.append(sms)
        return sms
    
    def get_sms_history(self, phone_number: str) -> list:
        """Get SMS history for a phone number"""
        return [sms for sms in self.sms_log if sms["phone_number"] == phone_number]

# Global tool instances
crm_tool = CRMTool()
ticket_tool = TicketTool()
payment_tool = PaymentTool()
sms_tool = SMSTool()
