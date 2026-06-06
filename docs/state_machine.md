# CredResolve AI - State Machine Documentation

## Overview

The CredResolve AI agent uses a LangGraph state machine with 11 states to orchestrate debt collection conversations. Each state has specific entry criteria, exit criteria, failure handling, and recovery paths.

## State Definitions

### 1. Greeting

**Purpose:** Welcome the borrower and establish initial contact

**Entry Criteria:**
- Start of conversation
- Phone number provided

**Exit Criteria:**
- Borrower responds to greeting
- Borrower refuses to engage

**Actions:**
- Check if returning customer (memory lookup)
- Generate personalized greeting
- Set initial context

**Failure Handling:**
- If borrower hangs up: End conversation
- If borrower refuses: End conversation politely

**Recovery Paths:**
- Retry greeting with different approach
- Offer callback at preferred time

**Output:**
- Greeting message
- User memory (if exists)
- Next state: Authentication or EndConversation

---

### 2. Authentication

**Purpose:** Verify borrower identity

**Entry Criteria:**
- From Greeting state
- Borrower willing to proceed

**Exit Criteria:**
- Identity verified successfully
- Identity verification fails

**Actions:**
- Fetch customer data from CRM
- Request name confirmation
- Validate phone number

**Failure Handling:**
- If customer not found: Request alternative contact
- If verification fails: End conversation

**Recovery Paths:**
- Request alternative verification method
- Manual verification by human agent

**Output:**
- Customer data
- Authentication status
- Next state: ContextGathering or EndConversation

---

### 3. ContextGathering

**Purpose:** Gather information about borrower's current situation

**Entry Criteria:**
- From Authentication
- Identity verified

**Exit Criteria:**
- Borrower provides situation details
- Borrower refuses to provide information

**Actions:**
- Explain outstanding amount
- Ask about current financial situation
- Inquire about payment ability
- Check user memory for preferences

**Failure Handling:**
- If borrower refuses: Escalate or end
- If insufficient information: Re-route to Diagnosis

**Recovery Paths:**
- Ask questions in different way
- Use user memory to guide conversation

**Output:**
- Borrower situation details
- Payment ability assessment
- Next state: Diagnosis or EndConversation

---

### 4. Diagnosis

**Purpose:** Analyze borrower's situation and determine appropriate path

**Entry Criteria:**
- From ContextGathering
- Sufficient context gathered

**Exit Criteria:**
- Path determined
- Analysis complete

**Actions:**
- Classify borrower intent
- Assess financial capability
- Evaluate risk level
- Determine recommended action

**Routing Logic:**
- High risk + long overdue → KnowledgeRetrieval
- Short overdue → Negotiation
- Need calculation → ToolExecution
- Dispute → KnowledgeRetrieval
- Escalation needed → Escalation

**Failure Handling:**
- If analysis unclear: Ask for more information
- If routing fails: Default to ToolExecution

**Recovery Paths:**
- Re-route to ContextGathering for more info
- Use default path

**Output:**
- Intent classification
- Risk assessment
- Recommended action
- Next state: KnowledgeRetrieval, ToolExecution, Negotiation, Escalation, or EndConversation

---

### 5. KnowledgeRetrieval

**Purpose:** Retrieve relevant information from knowledge base

**Entry Criteria:**
- From Diagnosis
- Need policy or guideline information

**Exit Criteria:**
- Knowledge retrieved successfully
- Retrieval fails

**Actions:**
- Query ChromaDB with relevant terms
- Retrieve top-k documents
- Format results for context
- Include source citations

**Failure Handling:**
- If retrieval fails: Proceed without knowledge
- If no results: Use fallback responses

**Recovery Paths:**
- Use cached knowledge if available
- Proceed with general responses

**Output:**
- Retrieved documents
- Formatted context
- Source citations
- Next state: ToolExecution or Negotiation

---

### 6. ToolExecution

**Purpose:** Execute relevant tools (payment calculation, SMS, etc.)

**Entry Criteria:**
- From Diagnosis or KnowledgeRetrieval
- Tool execution needed

**Exit Criteria:**
- Tools executed successfully
- Tool execution fails

**Actions:**
- Calculate settlement options
- Calculate EMI restructuring
- Send SMS reminders
- Create tickets if needed
- Log all tool calls

**Available Tools:**
- CRM Tool: Fetch customer data
- Payment Tool: Calculate amounts
- Ticket Tool: Create/update tickets
- SMS Tool: Send messages

**Failure Handling:**
- If tool fails: Log error and continue
- If calculation fails: Use manual fallback

**Recovery Paths:**
- Retry tool execution
- Use manual calculation
- Proceed without tool result

**Output:**
- Tool results
- Tool call logs
- Next state: Negotiation, Resolution, or Escalation

---

### 7. Negotiation

**Purpose:** Discuss payment terms and reach agreement

**Entry Criteria:**
- From ToolExecution or Diagnosis
- Options available to discuss

**Exit Criteria:**
- Agreement reached
- Negotiation breaks down
- Escalation requested

**Actions:**
- Present payment options
- Discuss terms and conditions
- Address borrower concerns
- Document promises-to-pay

**Negotiation Strategies:**
- Offer settlement discount
- Provide EMI restructuring
- Suggest partial payment
- Schedule payment plan

**Failure Handling:**
- If borrower refuses: Escalate
- If negotiation breaks: Offer callback
- If angry borrower: De-escalate

**Recovery Paths:**
- Offer alternative terms
- Provide more time
- Escalate to human agent

**Output:**
- Agreement status
- Payment terms
- Next state: Resolution, Escalation, FollowUp, or EndConversation

---

### 8. Escalation

**Purpose:** Handle cases that require human intervention

**Entry Criteria:**
- From Diagnosis, ToolExecution, or Negotiation
- Beyond agent authority or capability

**Exit Criteria:**
- Escalation ticket created
- Callback scheduled

**Actions:**
- Create escalation ticket
- Document conversation history
- Schedule callback with senior team
- Inform borrower of next steps

**Escalation Triggers:**
- Dispute not resolved
- Legal threat
- Regulatory complaint
- High-value account
- VIP customer
- Repeated refusal

**Failure Handling:**
- If ticket creation fails: Log for manual escalation
- If callback fails: Provide alternative contact

**Recovery Paths:**
- Manual escalation process
- Direct human handoff

**Output:**
- Ticket details
- Callback information
- Next state: Resolution, FollowUp, or EndConversation

---

### 9. Resolution

**Purpose:** Confirm agreement and document resolution

**Entry Criteria:**
- From Negotiation or Escalation
- Agreement reached

**Exit Criteria:**
- Confirmation sent
- Documentation complete

**Actions:**
- Confirm agreement details
- Send confirmation SMS
- Update customer records
- Log resolution

**Resolution Types:**
- Full payment committed
- Settlement accepted
- Payment plan agreed
- Dispute resolved

**Failure Handling:**
- If confirmation fails: Retry or manual follow-up
- If documentation fails: Log for manual entry

**Recovery Paths:**
- Re-send confirmation
- Manual documentation

**Output:**
- Confirmation details
- Resolution status
- Next state: FollowUp or EndConversation

---

### 10. FollowUp

**Purpose:** Schedule callback and document next steps

**Entry Criteria:**
- From Escalation or Resolution
- Follow-up needed

**Exit Criteria:**
- Callback scheduled
- Next steps documented

**Actions:**
- Schedule callback at preferred time
- Document next steps
- Set reminder
- Close current conversation

**Follow-up Types:**
- Payment reminder
- Settlement check
- Dispute follow-up
- Senior team callback

**Failure Handling:**
- If scheduling fails: Log for manual scheduling
- If no preferred time: Use default

**Recovery Paths:**
- Manual scheduling
- Default callback time

**Output:**
- Callback details
- Next steps
- Next state: EndConversation

---

### 11. EndConversation

**Purpose:** Close conversation and save to memory

**Entry Criteria:**
- From any state
- Conversation complete

**Exit Criteria:**
- Memory saved
- Conversation closed

**Actions:**
- Save conversation to memory
- Update user memory if needed
- Log promises-to-pay
- Track metrics
- Close conversation gracefully

**Memory Operations:**
- Save conversation turn
- Update user preferences
- Log promises
- Track state transitions

**Failure Handling:**
- If memory save fails: Log error
- If metrics fail: Continue without metrics

**Recovery Paths:**
- Retry memory save
- Log for manual entry

**Output:**
- Final response
- Memory save status
- Next state: END

---

## State Transition Matrix

| From State | To States | Conditions |
|------------|-----------|------------|
| Greeting | Authentication | Borrower willing |
| Greeting | EndConversation | Borrower refuses |
| Authentication | ContextGathering | Verified |
| Authentication | EndConversation | Not found |
| ContextGathering | Diagnosis | Info provided |
| ContextGathering | EndConversation | Refuses |
| Diagnosis | KnowledgeRetrieval | Need info |
| Diagnosis | ToolExecution | Need calculation |
| Diagnosis | Negotiation | Ready to discuss |
| Diagnosis | Escalation | Beyond authority |
| Diagnosis | EndConversation | No path |
| KnowledgeRetrieval | ToolExecution | Retrieved |
| KnowledgeRetrieval | Negotiation | Direct to discuss |
| ToolExecution | Negotiation | Have options |
| ToolExecution | Resolution | Auto-resolve |
| ToolExecution | Escalation | Failed |
| Negotiation | Resolution | Agreement |
| Negotiation | Escalation | Breakdown |
| Negotiation | FollowUp | Callback needed |
| Negotiation | EndConversation | Complete |
| Escalation | Resolution | Resolved |
| Escalation | FollowUp | Callback needed |
| Escalation | EndConversation | Complete |
| Resolution | FollowUp | Follow-up needed |
| Resolution | EndConversation | Complete |
| FollowUp | EndConversation | Always |

## Error Handling

### State-Level Errors
- Each state has try-catch blocks
- Errors logged with context
- Fallback to safe state

### Recovery Strategies
1. **Retry**: Re-execute state
2. **Fallback**: Use default response
3. **Escalate**: Route to human
4. **End**: Graceful termination

### Monitoring
- All state transitions logged
- Error rates tracked
- Recovery success measured
