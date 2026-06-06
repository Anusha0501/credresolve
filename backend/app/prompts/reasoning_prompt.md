You are analyzing the borrower's situation to determine the best course of action. Use the following framework to reason through the case.

## Current Situation
- Borrower State: {borrower_state}
- Outstanding Amount: {outstanding_amount}
- Overdue Days: {overdue_days}
- Risk Category: {risk_category}
- Previous Interactions: {previous_interactions}

## Borrower's Response
{borrower_response}

## Analysis Framework

### 1. Intent Classification
What is the borrower's intent?
- Willing to pay (needs assistance)
- Unable to pay (genuine hardship)
- Refusing to pay (dispute or unwillingness)
- Requesting more information
- Requesting escalation

### 2. Financial Assessment
Based on their response, assess:
- Can they pay now? (Yes/No)
- Can they pay in future? (Yes/No/Unsure)
- Do they need settlement? (Yes/No)
- Do they need restructuring? (Yes/No)

### 3. Risk Evaluation
- Is this a high-risk case for default?
- Is escalation needed?
- Is legal action appropriate?
- Are there regulatory concerns?

### 4. Recommended Action
Based on your analysis, recommend:
- **Payment Plan**: If willing but unable to pay full amount
- **Settlement Offer**: If eligible and appropriate
- **Restructuring**: If long-term payment issues
- **Dispute Resolution**: If dispute raised
- **Escalation**: If beyond your authority
- **Callback**: If more information needed
- **Legal Process**: If refusal continues

### 5. Next State
Determine the next state in the conversation:
- Negotiation: If discussing payment terms
- Resolution: If agreement reached
- Escalation: If escalation needed
- FollowUp: If callback scheduled
- EndConversation: If resolved or terminated

## Output Format
Provide your reasoning in the following format:

**Intent**: [classification]
**Financial Assessment**: [summary]
**Risk Level**: [low/medium/high]
**Recommended Action**: [action]
**Next State**: [state]
**Reasoning**: [brief explanation]
