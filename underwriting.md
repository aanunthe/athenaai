# PDF Policy Underwriting

## Problem Statement

Build an AI agent that:

1. **Takes a a PDF file** containing loan approval guidelines as input
2. **Takes loan application data** as input
3. **Outputs an approval decision** with reasoning

You'll receive a PDF with specific lending criteria (income thresholds, debt ratios, credit score requirements, etc.). Your agent must parse these rules and apply them to loan applications.

**Why this matters at Athena:**

Real-world lending policies are complex documents. Your agent needs to extract the right information and apply it correctly - just like production AI systems that process regulatory documents, contracts, and financial policies.

---

## Requirements

### Input 1: Policy PDF

You'll receive a PDF file called `loan_policy.pdf` with content like:

```
LOAN APPROVAL GUIDELINES

Credit Score Requirements:
- Score >= 720: Low risk (approve if debt-to-income < 40%)
- Score 650-719: Medium risk (approve if debt-to-income < 30%)
- Score < 650: High risk (deny unless income > $150k/year)

Income Requirements:
- Minimum annual income: $35,000
- Must be employed for at least 12 months

Debt-to-Income Ratio:
- Maximum DTI: 40% for low-risk applicants
- Maximum DTI: 30% for medium-risk applicants
- High-risk applicants: case-by-case basis

Special Cases:
- First-time homebuyers: Add 5% leniency to DTI limits
- Self-employed: Require 24 months employment history
```

### Input 2: Loan Application Data

```json
{
  "applicantId": "APP_001",
  "requestedAmount": 250000,
  "annualIncome": 85000,
  "monthlyDebt": 2100,
  "creditScore": 690,
  "employmentMonths": 18,
  "isFirstTimeBuyer": false,
  "isSelfEmployed": false
}
```

### Required Output Format

```
{
  "decision": "approved" | "denied",
  "reasoning": "Credit score 690 falls in medium-risk category (650-719) \n
     Debt-to-income ratio: 29.6% (within 30% limit for medium-risk) \n
     Employment: 18 months (meets 12-month minimum)",
  "riskLevel": "low" | "medium" | "high"
}
```


### Technical Requirements

**Language:** Any (Python, JavaScript/TypeScript, Go, Rust etc.)
**Tools:** Any (LLM/Coding Tools/Libraries, Infrastructure)

## Example Walkthrough


**Given PDF content:**
```
Credit Score >= 720: Low risk (approve if DTI < 40%)
Credit Score 650-719: Medium risk (approve if DTI < 30%)
```

**Given Application:**
```json
{
  "creditScore": 690,
  "annualIncome": 85000,
  "monthlyDebt": 2100
}
```

**Your Agent Could Output:**


```json
{
  "decision": "approved",
  "reasoning": "Applicant qualifies under medium-risk criteria with DTI of 29.6%",
  "appliedRules": [
    "Credit score 690 falls in medium-risk category (650-719)",
    "Debt-to-income ratio 29.6% is below the 30% threshold for medium-risk"
  ],
  "riskLevel": "medium"
}
```

---

## Deliverables

Submit a link to your github repo with
1. **Source code** 
2. **README**
   - What tools you used
   - What your thought process/architecture was
   - Potential future improvements and challenges
   - How to run your code

## Notes

* Underwriting policy pdf is available [here](loan_policy.pdf)
* Most LLMs have free api keys available. Ex) for gemini - https://aistudio.google.com/api-keys
