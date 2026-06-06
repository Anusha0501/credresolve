"""
Hindi Debt Collection Scenarios
These scenarios demonstrate the agent's ability to handle various debt collection situations
in Hindi and Hinglish while maintaining ethical practices.
"""

HINDI_SCENARIOS = {
    "scenario_1_payment_delay": {
        "name": "Payment Delay - भुगतान में देरी",
        "description": "Borrower has missed payment due to temporary financial difficulty",
        "phone_number": "+919876543210",
        "customer_data": {
            "name": "Rajesh Kumar",
            "due_amount": 45000.0,
            "loan_type": "Personal Loan",
            "risk_category": "medium",
            "overdue_days": 45
        },
        "conversation_flow": [
            {
                "state": "Greeting",
                "agent": "Namaste! Main CredResolve se bol raha hoon. Aapke loan account ke baare mein baat karni thi.",
                "user": "Haan, boliye."
            },
            {
                "state": "Authentication",
                "agent": "Verification ke liye aap apna naam confirm karein.",
                "user": "Mera naam Rajesh Kumar hai."
            },
            {
                "state": "ContextGathering",
                "agent": "Shukriya Rajesh ji. Aapka outstanding amount ₹45,000 hai. Batayiye ki payment kyun nahi hui?",
                "user": "Actually, last month mein job change hua tha, isliye payment delay ho gayi."
            },
            {
                "state": "Diagnosis",
                "agent": "Samajh gaya. Job change ke wajah se financial pressure hota hai. Ab aap nayi job pe hain?",
                "user": "Haan, nayi job mil gayi hai. Ab main payment kar sakta hoon."
            },
            {
                "state": "ToolExecution",
                "agent": "Accha hai. Main settlement option check kar raha hoon. Aap ₹31,500 mein settle kar sakte hain jo ₹13,500 bachayega.",
                "user": "Wah! Yeh toh accha offer hai."
            },
            {
                "state": "Negotiation",
                "agent": "Kya aap yeh settlement accept karna chahte hain?",
                "user": "Haan, main accept karta hoon."
            },
            {
                "state": "Resolution",
                "agent": "Bahut accha! Main aapko confirmation SMS bhej raha hoon. Thank you Rajesh ji.",
                "user": "Thank you."
            }
        ],
        "key_points": [
            "Empathetic response to job change situation",
            "Offered settlement option",
            "Clear communication of savings",
            "Professional closing"
        ]
    },

    "scenario_2_refusal_to_pay": {
        "name": "Refusal to Pay - भुगतान से इनकार",
        "description": "Borrower refuses to pay claiming inability",
        "phone_number": "+919123456789",
        "customer_data": {
            "name": "Priya Sharma",
            "due_amount": 75000.0,
            "loan_type": "Home Loan EMI",
            "risk_category": "high",
            "overdue_days": 90
        },
        "conversation_flow": [
            {
                "state": "Greeting",
                "agent": "Namaste Priya ji, CredResolve se baat kar raha hoon.",
                "user": "Haan, boliye."
            },
            {
                "state": "Authentication",
                "agent": "Verification ke liye aap apna naam confirm karein.",
                "user": "Priya Sharma."
            },
            {
                "state": "ContextGathering",
                "agent": "Aapka outstanding amount ₹75,000 hai. Payment kyun nahi hui?",
                "user": "Main payment nahi kar sakti. Paisa nahi hai."
            },
            {
                "state": "Diagnosis",
                "agent": "Main samajhta hoon ki financial problems hoti hain. Lekin kuch solution dhundhna hoga. Kya aap kuch amount pay kar sakti hain?",
                "user": "Abhi toh bilkul nahi kar sakti."
            },
            {
                "state": "Negotiation",
                "agent": "Theek hai, main aapke case ko senior team ko escalate karunga. Wo aap se baat karenge.",
                "user": "Theek hai."
            },
            {
                "state": "Escalation",
                "agent": "Main ticket create kar diya hai. Senior team 24 ghante mein aapko call karenge.",
                "user": "OK."
            },
            {
                "state": "FollowUp",
                "agent": "Thank you Priya ji. Hum aapki help karna chahte hain.",
                "user": "Haan."
            }
        ],
        "key_points": [
            "Maintained politeness despite refusal",
            "Avoided harassment or threats",
            "Escalated appropriately",
            "Offered senior team assistance"
        ]
    },

    "scenario_3_payment_dispute": {
        "name": "Payment Dispute - भुगतान विवाद",
        "description": "Borrower disputes the amount claimed",
        "phone_number": "+919876543211",
        "customer_data": {
            "name": "Amit Singh",
            "due_amount": 25000.0,
            "loan_type": "Credit Card",
            "risk_category": "low",
            "overdue_days": 15
        },
        "conversation_flow": [
            {
                "state": "Greeting",
                "agent": "Namaste Amit ji, CredResolve se bol raha hoon.",
                "user": "Haan, kya baat hai?"
            },
            {
                "state": "Authentication",
                "agent": "Verification ke liye naam confirm karein.",
                "user": "Amit Singh."
            },
            {
                "state": "ContextGathering",
                "agent": "Aapka outstanding ₹25,000 hai. Payment kab karega?",
                "user": "Yeh amount galat hai. Maine last month ₹20,000 pay kiya tha."
            },
            {
                "state": "KnowledgeRetrieval",
                "agent": "Dispute raise karne ke liye main policy check kar raha hoon.",
                "user": "Haan, please check."
            },
            {
                "state": "ToolExecution",
                "agent": "Main dispute ticket create kar raha hoon. Aapko payment receipt bhejni hogi.",
                "user": "Theek hai, main receipt bhej dunga."
            },
            {
                "state": "Escalation",
                "agent": "Ticket create ho gaya. Investigation team 5 working days mein check karenge.",
                "user": "Accha, thank you."
            },
            {
                "state": "FollowUp",
                "agent": "Jab receipt bhej dijiye toh batana. Hum resolve kar denge.",
                "user": "Bilkul."
            }
        ],
        "key_points": [
            "Acknowledged dispute seriously",
            "Followed dispute policy",
            "Requested supporting documents",
            "Provided clear timeline"
        ]
    },

    "scenario_4_settlement_negotiation": {
        "name": "Settlement Negotiation - समझौता वार्ता",
        "description": "Borrower negotiates for better settlement terms",
        "phone_number": "+919876543210",
        "customer_data": {
            "name": "Rajesh Kumar",
            "due_amount": 45000.0,
            "loan_type": "Personal Loan",
            "risk_category": "medium",
            "overdue_days": 45
        },
        "conversation_flow": [
            {
                "state": "Greeting",
                "agent": "Namaste Rajesh ji, CredResolve se baat kar raha hoon.",
                "user": "Haan, boliye."
            },
            {
                "state": "ContextGathering",
                "agent": "Aapka outstanding ₹45,000 hai. Settlement offer: ₹31,500.",
                "user": "Yeh zyada hai. Kya kam ho sakta hai?"
            },
            {
                "state": "Diagnosis",
                "agent": "Main check karta hoon ki aapke case mein kya possible hai.",
                "user": "Please check."
            },
            {
                "state": "ToolExecution",
                "agent": "EMI restructuring option bhi hai. 6 months mein ₹7,500 per month.",
                "user": "Yeh better hai. Maine yeh choose karna hai."
            },
            {
                "state": "Negotiation",
                "agent": "Accha choice hai. Processing fee 2% hogi. Total ₹45,900.",
                "user": "Theek hai, main agree karta hoon."
            },
            {
                "state": "Resolution",
                "agent": "Bahut accha! Confirmation SMS bhej diya. First installment 15 din mein.",
                "user": "Thank you."
            }
        ],
        "key_points": [
            "Listened to borrower's negotiation",
            "Offered alternative (EMI restructuring)",
            "Clearly explained all charges",
            "Confirmed agreement"
        ]
    },

    "scenario_5_angry_borrower": {
        "name": "Angry Borrower - गुस्सैल उधारकर्ता",
        "description": "Borrower is angry and upset",
        "phone_number": "+919123456789",
        "customer_data": {
            "name": "Priya Sharma",
            "due_amount": 75000.0,
            "loan_type": "Home Loan EMI",
            "risk_category": "high",
            "overdue_days": 90
        },
        "conversation_flow": [
            {
                "state": "Greeting",
                "agent": "Namaste Priya ji, CredResolve se bol raha hoon.",
                "user": "Aap log roj call karte ho! Main bahut pareshan hoon!"
            },
            {
                "state": "Authentication",
                "agent": "Main samajhta hoon ki aap pareshan hain. Verification ke liye naam bataiye.",
                "user": "Priya Sharma hai, lekin please call mat karo!"
            },
            {
                "state": "ContextGathering",
                "agent": "Maaf kijiye agar pareshan hui. Main aapki help karna chahta hoon. Kya problem hai?",
                "user": "Mera husband job lose kar diya, hum pareshan hain, aur aap log pressure daal rahe ho!"
            },
            {
                "state": "Diagnosis",
                "agent": "Bahut dukh hua yeh sunkar. Main aapko disturb nahi karna chahta. Kya main callback schedule kar doon?",
                "user": "Haan, please kal evening 6 baje call karna."
            },
            {
                "state": "ToolExecution",
                "agent": "Theek hai, main kal 6 baje callback schedule kar raha hoon. Abhi call nahi karunga.",
                "user": "Thank you."
            },
            {
                "state": "FollowUp",
                "agent": "Kal baat karte hain Priya ji. Take care.",
                "user": "Bye."
            }
        ],
        "key_points": [
            "Acknowledged anger without being defensive",
            "Showed empathy for difficult situation",
            "Respected request to stop calling",
            "Scheduled callback at preferred time",
            "Maintained professionalism throughout"
        ]
    }
}

def get_scenario(scenario_id: str):
    """Get a specific scenario by ID"""
    return HINDI_SCENARIOS.get(scenario_id)

def get_all_scenarios():
    """Get all scenarios"""
    return HINDI_SCENARIOS

def get_scenario_list():
    """Get list of scenario IDs and names"""
    return [
        {"id": key, "name": value["name"]}
        for key, value in HINDI_SCENARIOS.items()
    ]
