"""
sebi_rules.py - Statutory Regulatory Validation Engine
Enforces SEBI Intermediary Regulations and Advertisement Codes.
"""
import re

# Official SEBI Registration Alphanumeric Patterns
SEBI_REG_PATTERNS = {
    "Investment Adviser (IA)": r"\bINA\d{9}\b",
    "Research Analyst (RA)": r"\bINH\d{9}\b",
    "Stock Broker / Trading Member": r"\bINZ\d{9}\b",
    "Portfolio Management Services (PMS)": r"\bINP\d{9}\b",
    "Mutual Fund": r"\bMF/\d{3}/\d{2}/\d{2}\b"
}

# Strictly Prohibited Commercial & Fraudulent Claims under SEBI Circulars
PROHIBITED_CLAIM_PATTERNS = [
    (r"(guarantee\w*|100%|sure\s*shot)\s*(return|profit|gain)", "Guaranteed profit promise (Direct violation of SEBI Advertisement Code)"),
    (r"(double|triple)\s*(money|investment|funds|rupees)", "Unrealistic multiplier claim (Ponzi / illegal collective investment scheme pattern)"),
    (r"(zero\s*loss|no\s*risk|loss\s*recovery)", "Zero-risk or loss-recovery assertion (Misleading representation under SEBI PFUTP Regulations)"),
    (r"(vip|premium|jackpot|sure)\s*(group|call|tip|channel)", "Unregistered advisory / tip-channel solicitation"),
    (r"(sebi\s*(approved|certified|guaranteed)\s*(profit|return|scheme))", "False regulatory endorsement claim (SEBI never endorses or guarantees profits)")
]

def extract_claimed_registration(text: str) -> dict:
    """Extracts and verifies any claimed SEBI registration strings against official nomenclature."""
    if not text:
        return {"found": False, "raw_string": None, "category": None, "is_valid_format": False}
    
    for category, pattern in SEBI_REG_PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return {
                "found": True,
                "raw_string": match.group(0).upper(),
                "category": category,
                "is_valid_format": True
            }
            
    # Check for fake/garbage formats like SEBI/VIP/101 or SEBI-GOV-2026
    fake_match = re.search(r"\bSEBI[/-][A-Za-z0-9/-]{3,15}\b", text, re.IGNORECASE)
    if fake_match:
        return {
            "found": True,
            "raw_string": fake_match.group(0),
            "category": "Unrecognized / Fabricated Format",
            "is_valid_format": False
        }
        
    return {"found": False, "raw_string": None, "category": None, "is_valid_format": False}

def audit_sebi_compliance(text: str) -> dict:
    """Audits text against SEBI statutory prohibitions and returns an explainable risk breakdown."""
    violations = []
    
    for pattern, description in PROHIBITED_CLAIM_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            violations.append(description)
            
    reg_audit = extract_claimed_registration(text)
    
    # Calculate Regulatory Severity Penalty
    penalty_score = len(violations) * 25
    if reg_audit["found"] and not reg_audit["is_valid_format"]:
        penalty_score += 40
        violations.append(f"Fabricated SEBI registration format detected: '{reg_audit['raw_string']}'")
        
    penalty_score = min(100, penalty_score)
    
    return {
        "regulatory_penalty": penalty_score,
        "violations": violations,
        "registration_status": reg_audit
    }
