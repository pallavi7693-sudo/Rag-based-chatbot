import re
from typing import Dict, Any

ADVISORY_PATTERNS = [
    r"\bshould\s+i\s+(?:invest|buy|sell|switch|redeem|enter|exit)\b",
    r"\bwhich\s+fund\s+is\s+(?:better|best|superior|good|recommended|safer)\b",
    r"\brecommend\s+(?:a|any|me|some)\s+fund\b",
    r"\bis\s+it\s+a\s+good\s+time\s+to\s+(?:invest|buy)\b",
    r"\b(?:predict|forecast|expect)\s+(?:return|returns|performance|growth|profit)\b",
    r"\bwill\s+this\s+fund\s+(?:give|generate|outperform|beat|double|increase)\b",
    r"\badvice\s+me\b",
    r"\bgive\s+me\s+(?:investment\s+advice|tips|suggestions)\b",
    r"\bwhat\s+should\s+i\s+do\b",
    r"\bcompare\s+performance\s+with\b",
    r"\bhow\s+much\s+(?:return|profit)\s+will\s+i\s+get\b",
    r"\bmy\s+portfolio\b",
    r"\bfuture\s+returns\b",
    r"\bis\s+this\s+fund\s+safe\s+for\s+my\s+money\b"
]

# Patterns for PII detection (PAN, Aadhaar, Phone numbers, OTPs, Email, Bank Account)
PII_PATTERNS = [
    (r"\b[A-Z]{5}[\-\s\.]*[0-9]{4}[\-\s\.]*[A-Z]{1}\b", "PAN Card Number"),
    (r"\b\d{4}[\-\s\.]*\d{4}[\-\s\.]*\d{4}\b", "Aadhaar Number"),
    (r"\b(?:\+91[\-\s]?|0)?[6-9]\d{9}\b", "Phone Number"),
    (r"\b\d{4,6}\s*(?:is\s+my|otp|pin|password)\b", "OTP/PIN"),
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", "Email Address"),
    (r"\b(?:account|acct|a/c)\s*(?:no|number|num)?\s*[:=]?\s*\d{9,18}\b", "Bank Account Number")
]

REFUSAL_MESSAGE = (
    "I am a facts-only assistant and am strictly prohibited from providing investment advice, "
    "opinions, or fund recommendations. To learn more about mutual fund investing and regulatory "
    "guidelines, please visit the official AMFI Investor Education portal: "
    "https://www.amfiindia.com/investor-corner/knowledge-center/what-is-mutual-fund.html"
)

PII_MESSAGE = (
    "Security & Privacy Notice: For your security, this assistant does not collect, store, or process "
    "sensitive personal information such as PAN, Aadhaar, bank account numbers, OTPs, email addresses, "
    "or phone numbers. Please do not enter sensitive financial data into this chat."
)

def check_query(query: str) -> Dict[str, Any]:
    query_lower = query.lower()
    
    # 1. Check for PII / Sensitive Data
    for pattern, pii_type in PII_PATTERNS:
        if re.search(pattern, query, re.IGNORECASE):
            return {
                "is_refused": True,
                "reason": f"PII Detected: {pii_type}",
                "message": PII_MESSAGE,
                "educational_link": "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpi=yes"
            }
            
    # 2. Check for Advisory / Speculative / Opinion queries
    for pattern in ADVISORY_PATTERNS:
        if re.search(pattern, query_lower):
            return {
                "is_refused": True,
                "reason": "Advisory Query Refused",
                "message": REFUSAL_MESSAGE,
                "educational_link": "https://www.amfiindia.com/investor-corner/knowledge-center/what-is-mutual-fund.html"
            }
            
    # 3. Keyword heuristic for advisory words without pattern matching
    advisory_words = ["should i buy", "which is better", "guaranteed return", "best mutual fund to invest", "give me advice"]
    for word in advisory_words:
        if word in query_lower:
            return {
                "is_refused": True,
                "reason": "Advisory Query Refused",
                "message": REFUSAL_MESSAGE,
                "educational_link": "https://www.amfiindia.com/investor-corner/knowledge-center/what-is-mutual-fund.html"
            }

    return {
        "is_refused": False,
        "reason": "Valid Factual Query",
        "message": "",
        "educational_link": ""
    }
