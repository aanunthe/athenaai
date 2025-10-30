import json
import sys
import os

def process_application(application_data):
    try:
        annual_income = application_data['annualIncome']
        credit_score = application_data['creditScore']
        monthly_debt = application_data['monthlyDebt']
        employment_months = application_data['employmentMonths']
        is_first_time_buyer = application_data['isFirstTimeBuyer']
        is_self_employed = application_data['isSelfEmployed']
        requested_amount = application_data['requestedAmount']
    except KeyError as e:
        return {
            "decision": "denied",
            "reasoning": f"Missing required application field: {e}",
            "riskLevel": "high"
        }

    reasoning = []
    
    if annual_income < 35000:
        reasoning.append(f"DENIED: Annual income ${annual_income:,.2f} is below the ${35000:,.2f} minimum.")
        return {"decision": "denied", "reasoning": "\n".join(reasoning), "riskLevel": "high"}
        
    if credit_score < 600:
        reasoning.append(f"DENIED: Credit score {credit_score} is below the 600 minimum requirement.")
        return {"decision": "denied", "reasoning": "\n".join(reasoning), "riskLevel": "high"}

    if annual_income == 0:
         reasoning.append("DENIED: Annual income is $0, cannot calculate DTI.")
         return {"decision": "denied", "reasoning": "\n".join(reasoning), "riskLevel": "high"}
         
    dti = (monthly_debt * 12) / annual_income
    reasoning.append(f"INFO: Debt-to-Income (DTI) calculated at {dti:.1%}.")

    if credit_score >= 720:
        risk_level = "low"
        dti_limit = 0.40
        emp_req_months = 12
        max_loan = 500000
        reasoning.append(f"INFO: Credit score {credit_score} qualifies for Tier 1 (Low Risk).")
    
    elif 650 <= credit_score <= 719:
        risk_level = "medium"
        dti_limit = 0.30
        emp_req_months = 18
        max_loan = 350000
        reasoning.append(f"INFO: Credit score {credit_score} qualifies for Tier 2 (Medium Risk).")
    
    else:
        risk_level = "high"
        dti_limit = 0.25
        emp_req_months = 24
        max_loan = 200000
        reasoning.append(f"INFO: Credit score {credit_score} qualifies for Tier 3 (High Risk).")
        
        if annual_income < 150000:
            reasoning.append(f"DENIED: High-risk applicants with income below $150,000 are automatically denied.")
            return {"decision": "denied", "reasoning": "\n".join(reasoning), "riskLevel": risk_level}
        else:
             reasoning.append(f"INFO: High-risk applicant income ${annual_income:,.2f} exceeds $150,000; proceeding with review.")

    if is_self_employed:
        reasoning.append(f"INFO: Applicant is self-employed, requires 24 months history.")
        emp_req_months = 24
    
    if employment_months < emp_req_months:
        reasoning.append(f"DENIED: Employment history of {employment_months} months is insufficient. Required: {emp_req_months} months.")
        return {"decision": "denied", "reasoning": "\n".join(reasoning), "riskLevel": risk_level}
    else:
         reasoning.append(f"PASS: Employment history of {employment_months} months meets the {emp_req_months}-month requirement.")

    if requested_amount > max_loan:
        reasoning.append(f"DENIED: Requested amount ${requested_amount:,.2f} exceeds the maximum of ${max_loan:,.2f} for this risk tier.")
        return {"decision": "denied", "reasoning": "\n".join(reasoning), "riskLevel": risk_level}
    else:
         reasoning.append(f"PASS: Requested amount ${requested_amount:,.2f} is within the ${max_loan:,.2f} maximum.")

    original_dti_limit = dti_limit
    if is_first_time_buyer:
        dti_limit += 0.05
        reasoning.append(f"INFO: First-time homebuyer status applied. DTI limit increased from {original_dti_limit:.1%} to {dti_limit:.1%}.")
    
    if dti > dti_limit:
        reasoning.append(f"DENIED: DTI of {dti:.1%} exceeds the {dti:.1%} limit.")
        return {"decision": "denied", "reasoning": "\n".join(reasoning), "riskLevel": risk_level}
    else:
        reasoning.append(f"PASS: DTI of {dti:.1%} is within the {dti:.1%} limit.")
    
    reasoning.insert(0, "APPROVED: Applicant meets all criteria.")
    return {
        "decision": "approved",
        "reasoning": "\n".join(reasoning),
        "riskLevel": risk_level
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python underwrite.py <path_to_application.json>", file=sys.stderr)
        sys.exit(1)

    json_file_path = sys.argv[1]

    if not os.path.exists(json_file_path):
        print(f"Error: File not found at {json_file_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(json_file_path, 'r') as f:
            application_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    result = process_application(application_data)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()