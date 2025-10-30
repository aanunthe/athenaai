# Athena PDF Policy Underwriting Agent

This project implements a simple, no-dependency Python agent to solve the underwriting challenge. The agent takes a loan application in JSON format and applies the business logic derived from the `loan_policy.pdf` to produce an approval or denial decision.

## 1. Tools Used

* **Language:** Python 3 (no external libraries required)
* **Tools:** Only built-in `json` (for parsing the input file) and `sys` (for reading command-line arguments).

## 2. Thought Process & Architecture

The core requirement was to build an agent that applies rules from a PDF to a loan application, with a key user constraint of "minimum complexity for execution."

My architecture choice was to **transcribe the rules from the PDF directly into Python code** rather than using an LLM or PDF-parsing library to extract the rules dynamically.

**Rationale:**

1.  **Minimum Complexity & Robustness:** A dynamic parsing approach (e.g., feeding the PDF to an LLM API) introduces many points of failure. It would require network access, API key management, prompt engineering, and handling for "hallucinated" or misinterpreted rules. A single, self-contained Python script has zero external dependencies and is 100% deterministic.
2.  **Stability:** The `loan_policy.pdf` is a fixed document. Hard-coding its logic into a "rules engine" function is the standard, most reliable way to implement stable business logic.
3.  **Performance:** Executing local Python logic is instantaneous. An API call to an LLM would add significant latency to every decision.

The script (`underwrite.py`) is structured as follows:

1.  A `main()` function handles file I/O: it reads the JSON file path from the command line, opens it, and parses the JSON.
2.  A core `process_application(application_data)` function contains all the business logic.
3.  The logic inside `process_application` is ordered by priority, exactly as in the policy document:
    * **Step 1:** Check for automatic denials (e.g., income < $35k, credit score < 600).
    * **Step 2:** Calculate DTI.
    * **Step 3:** Determine the applicant's risk tier.
    * **Step 4:** Check tier-specific rules (employment, max loan, special high-risk rules).
    * **Step 5:** Apply special circumstances (e.g., DTI leniency for first-time buyers).
    * **Step 6:** Make the final DTI check against the (potentially adjusted) limit.
4.  As it executes, the script builds a list of `reasoning` strings, which are then joined to form the final output. This provides a clear audit trail for the decision.
5.  The script prints the final decision dictionary to `stdout` as a formatted JSON string.

## 3. How to Run Your Code

1.  Ensure you have Python 3 installed.
2.  Save the code above as `underwrite.py`.
3.  Save the example application as `application.json`.
4.  Run the script from your terminal, passing the `application.json` file as an argument:

    ```bash
    python underwrite.py application.json
    ```

**Example Output (using `application.json`):**

```json
{
  "decision": "approved",
  "reasoning": "APPROVED: Applicant meets all criteria.\nINFO: Debt-to-Income (DTI) calculated at 29.6%. [cite: 36, 40]\nINFO: Credit score 690 qualifies for Tier 2 (Medium Risk). [cite: 12]\nPASS: Employment history of 18 months meets the 18-month requirement. [cite: 10, 16, 25, 33]\nPASS: Requested amount $250,000.00 is within the $350,000.00 maximum. [cite: 8, 14, 23]\nPASS: DTI of 29.6% is within the 30.0% limit. [cite: 7, 13, 21]",
  "riskLevel": "medium"
}