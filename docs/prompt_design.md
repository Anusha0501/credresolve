# CredResolve AI - Prompt Design Documentation

## Overview

This document explains the rationale behind the prompt design for the CredResolve AI Debt Collection Agent. The prompts are designed to ensure ethical, effective, and compliant debt collection conversations.

## Prompt Library Structure

The prompt library consists of 4 main prompts:

1. **System Prompt** - Defines the agent's role and core principles
2. **Context Prompt** - Guides context gathering and information synthesis
3. **Reasoning Prompt** - Structured framework for decision-making
4. **Evaluation Prompt** - Quality and compliance assessment

## 1. System Prompt

### Purpose
Defines the agent's identity, core principles, and behavioral guidelines.

### Design Rationale

**Role Definition**
- Clear identity as "CredResolve AI"
- Professional debt collection agent persona
- Establishes authority and trust

**Core Principles Section**
- **Ethical Communication**: Sets the tone for all interactions
- **RBI Compliance**: Ensures regulatory adherence
- **Empathy First**: Human-centered approach
- **Solution-Oriented**: Focus on resolution, not just collection
- **Transparency**: Builds trust through clarity

**Language Support**
- Explicitly mentions Hindi and Hinglish
- Adapts to borrower preference
- Ensures cultural sensitivity

**Key Responsibilities**
- Clear scope of work
- Defines what the agent should do
- Sets expectations for interactions

**Prohibited Behaviors**
- Explicit negative constraints
- Prevents harmful actions
- Ensures compliance

### Key Design Decisions

1. **Positive Framing**: Focus on what TO DO rather than what NOT to do
2. **Specific Examples**: Concrete guidelines (e.g., contact hours)
3. **Cultural Context**: Indian context with RBI guidelines
4. **Bilingual Support**: Explicit Hindi/Hinglish mention
5. **Ethical Guardrails**: Clear prohibited behaviors

### Usage
Used as the base system prompt for all conversations. Sets the foundation for agent behavior.

---

## 2. Context Prompt

### Purpose
Guides the agent in gathering and synthesizing context from multiple sources.

### Design Rationale

**Template Structure**
- Uses placeholders for dynamic content
- Allows injection of customer data, history, memory
- Flexible for different conversation stages

**Borrower Information Section**
- Customer data from CRM
- Provides factual basis for conversation
- Helps personalize interaction

**Conversation History**
- Previous interactions
- Avoids repetition
- Maintains continuity

**User Memory**
- Preferences and patterns
- Enables personalization
- Improves efficiency

**Current State**
- Where in the conversation flow
- Guides appropriate responses
- Ensures state awareness

**Instructions Section**
- Step-by-step guidance
- Clear action items
- Structured approach

**Response Guidelines**
- Conciseness requirement
- One question at a time
- Documentation emphasis

### Key Design Decisions

1. **Template-Based**: Dynamic content injection
2. **Multi-Source**: Combines CRM, memory, history
3. **Action-Oriented**: Clear instructions
4. **Documentation Focus**: Emphasizes logging
5. **User-Centric**: Focuses on borrower needs

### Usage
Used in ContextGathering state to guide information collection and synthesis.

---

## 3. Reasoning Prompt

### Purpose
Provides a structured framework for analyzing borrower situations and making decisions.

### Design Rationale

**Current Situation Section**
- Borrower state and data
- Outstanding amount and risk
- Previous interactions
- Provides complete context

**Analysis Framework**
- **Intent Classification**: Understanding borrower's position
- **Financial Assessment**: Capability evaluation
- **Risk Evaluation**: Default and escalation risk
- **Recommended Action**: Decision output
- **Next State**: State machine routing

**Structured Output Format**
- Consistent format for all analyses
- Easy to parse programmatically
- Clear decision trail

### Key Design Decisions

1. **Structured Analysis**: Step-by-step framework
2. **Multiple Dimensions**: Intent, financial, risk
3. **Action-Oriented**: Focuses on next steps
4. **State Machine Integration**: Includes next state
5. **Explainable**: Requires reasoning field

### Usage
Used in Diagnosis state to analyze borrower situation and determine next actions.

---

## 4. Evaluation Prompt

### Purpose
Assesses conversation quality and compliance for monitoring and improvement.

### Design Rationale

**Conversation Transcript**
- Full conversation context
- Enables comprehensive evaluation
- Captures interaction flow

**Evaluation Criteria**
- **Ethical Compliance**: Pass/Fail for regulatory adherence
- **Effectiveness**: 1-5 scale for outcome quality
- **Empathy Score**: 1-5 scale for human-centered approach
- **Solution Quality**: 1-5 scale for appropriateness
- **Documentation Quality**: 1-5 scale for record-keeping

**Compliance Checklist**
- Binary checklist for key requirements
- Easy to verify
- Covers all critical aspects

**Overall Assessment**
- Summary judgment
- Strengths and weaknesses
- Actionable recommendations

### Key Design Decisions

1. **Multi-Dimensional**: Evaluates multiple aspects
2. **Quantitative**: Uses scales for measurement
3. **Binary Compliance**: Clear pass/fail for regulations
4. **Actionable**: Provides recommendations
5. **Comprehensive**: Covers all important aspects

### Usage
Used for post-conversation evaluation, quality assurance, and agent performance monitoring.

---

## Prompt Engineering Principles

### 1. Clarity
- Clear, unambiguous instructions
- Specific examples where needed
- Avoid vague language

### 2. Context
- Provide relevant background
- Include necessary data
- Set appropriate scope

### 3. Structure
- Use sections and headings
- Numbered lists for sequences
- Consistent formatting

### 4. Constraints
- Explicit boundaries
- Clear do's and don'ts
- Specific limitations

### 5. Cultural Sensitivity
- Indian context
- Hindi language support
- RBI compliance
- Cultural norms

### 6. Ethical Guardrails
- Prohibited behaviors
- Compliance requirements
- Privacy protection
- Anti-harassment

### 7. Actionability
- Clear next steps
- Specific instructions
- Measurable outcomes

### 8. Flexibility
- Template-based for dynamic content
- Adaptable to different situations
- Scalable design

## Prompt Integration

### In LangGraph States

```
Greeting → System Prompt
Authentication → System Prompt
ContextGathering → Context Prompt
Diagnosis → Reasoning Prompt
KnowledgeRetrieval → Context Prompt
ToolExecution → System Prompt
Negotiation → Reasoning Prompt
Escalation → System Prompt
Resolution → System Prompt
FollowUp → Context Prompt
EndConversation → Evaluation Prompt
```

### Dynamic Content Injection

Prompts use template variables for dynamic content:
- `{customer_data}` - CRM data
- `{conversation_history}` - Previous interactions
- `{user_memory}` - Stored preferences
- `{current_state}` - State machine state
- `{borrower_response}` - Latest user input
- `{conversation_transcript}` - Full conversation

## Testing and Iteration

### Testing Approach
1. **Unit Testing**: Each prompt tested individually
2. **Integration Testing**: Prompts tested in state machine
3. **Scenario Testing**: Tested with Hindi scenarios
4. **Compliance Testing**: Verified against RBI guidelines

### Iteration Process
1. Draft initial prompts
2. Test with sample conversations
3. Evaluate outputs
4. Refine based on results
5. Repeat until satisfactory

### Success Metrics
- Response relevance
- Compliance adherence
- Empathy demonstration
- Solution appropriateness
- Documentation completeness

## Future Enhancements

### Potential Improvements
1. **Few-Shot Examples**: Add example conversations
2. **Chain of Thought**: Explicit reasoning steps
3. **Dynamic Prompts**: Adapt based on conversation
4. **A/B Testing**: Compare prompt variations
5. **User Feedback**: Incorporate borrower feedback

### Advanced Features
1. **Sentiment Analysis**: Adjust based on borrower emotion
2. **Risk-Based Prompts**: Different prompts for risk levels
3. **Personalization**: More individualized prompts
4. **Multi-Turn Context**: Better conversation memory
5. **Learning**: Improve from past conversations

## Conclusion

The prompt design for CredResolve AI emphasizes:
- **Ethical behavior** through clear guidelines
- **Cultural sensitivity** with Hindi support
- **Regulatory compliance** with RBI guidelines
- **Structured reasoning** for decision-making
- **Quality assurance** through evaluation

The prompts are designed to be clear, actionable, and adaptable while maintaining strict ethical and compliance standards.
