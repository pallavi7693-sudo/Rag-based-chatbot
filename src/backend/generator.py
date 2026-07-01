import os
import re
from typing import List, Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# Default Groq API Key provided by user (can be overridden via environment variables or .env)
DEFAULT_GROQ_API_KEY = "your-groq-api-key-here"

def _get_groq_client():
    if not GROQ_AVAILABLE:
        return None
    api_key = os.environ.get("GROQ_API_KEY", DEFAULT_GROQ_API_KEY)
    if not api_key or api_key == "your-groq-api-key-here":
        return None
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        print(f"Failed to initialize Groq client: {e}")
        return None

def _enforce_three_sentences(text: str) -> str:
    text = text.strip()
    # Basic sentence splitter that avoids splitting on common abbreviations like Rs., vs., approx., etc.
    sentences = re.split(r'(?<!\bRs)(?<!\bapprox)(?<!\be\.g)(?<!\bi\.e)(?<!\bvs)\.\s+|\?\s+|\!\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return text
        
    # Take at most 3 sentences
    top_3 = sentences[:3]
    formatted_text = ". ".join(top_3)
    if not formatted_text.endswith(".") and not formatted_text.endswith("!") and not formatted_text.endswith("?"):
        formatted_text += "."
        
    return formatted_text

def _generate_with_groq(query: str, chunk_content: str, scheme_name: str) -> str:
    client = _get_groq_client()
    if not client:
        return None
        
    system_prompt = (
        "You are FundIQ, a strict facts-only mutual fund FAQ assistant for ICICI Prudential schemes. "
        "Your strict regulatory instructions are:\n"
        "1. Answer the user query clearly and directly using ONLY the provided official factual context.\n"
        "2. Do NOT invent numbers, fees, or rules. Never provide investment advice, recommendations, or return predictions.\n"
        "3. CRITICAL: Your entire response MUST be at most 3 sentences long. Be concise and authoritative.\n"
        "4. Do NOT include URLs or citation links in your output text (the system automatically appends the official citation badge and date footer)."
    )
    
    user_prompt = f"Official Factual Context ({scheme_name}):\n{chunk_content}\n\nUser Question:\n{query}"
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
            max_tokens=256,
        )
        answer = completion.choices[0].message.content.strip()
        # Enforce 3 sentences safety check on LLM output
        return _enforce_three_sentences(answer)
    except Exception as e:
        err_str = str(e).lower()
        if "429" in err_str or "rate limit" in err_str or "quota" in err_str:
            print(f"[RATE LIMIT] Groq free tier limit reached (Limits: 30 RPM / 1,000 RPD / 12K TPM / 100K TPD). Switching instantly to local extractive fallback...")
        else:
            print(f"[WARN] Groq generation failed ({e}). Switching instantly to local extractive fallback...")
        return None

def generate_response(query: str, retrieved_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not retrieved_chunks:
        return {
            "answer": "We could not find verified factual information regarding your query in the official ICICI Prudential mutual fund corpus. Please consult official AMC or AMFI documents for verified details.",
            "citation_url": "https://www.icicipruamc.com/downloads/sid-kim",
            "last_updated": "July 2026",
            "scheme_referenced": "General / AMC"
        }
        
    # Pick the highest scoring chunk
    top_chunk = retrieved_chunks[0]
    content = top_chunk.get("content", "")
    source_url = top_chunk.get("source_url", "https://www.icicipruamc.com")
    last_updated = top_chunk.get("last_updated", "July 2026")
    scheme = top_chunk.get("scheme", "ICICI Prudential AMC")
    
    # Attempt LLM generation using Groq API
    answer = _generate_with_groq(query, content, scheme)
    
    # Fallback to extractive generator if Groq is unavailable
    if not answer:
        answer = _enforce_three_sentences(content)
    
    return {
        "answer": answer,
        "citation_url": source_url,
        "last_updated": last_updated,
        "scheme_referenced": scheme
    }

def format_final_reply(guardrail_res: Dict[str, Any], gen_res: Dict[str, Any]) -> Dict[str, Any]:
    if guardrail_res.get("is_refused", False):
        msg = _enforce_three_sentences(guardrail_res.get("message", ""))
        return {
            "is_refused": True,
            "refusal_reason": guardrail_res.get("reason", "Query Refused"),
            "answer": msg,
            "citation_url": guardrail_res.get("educational_link", "https://www.amfiindia.com/investor-corner/knowledge-center/what-is-mutual-fund.html"),
            "last_updated": "July 2026",
            "footer": "Last updated from sources: July 2026",
            "scheme_referenced": "AMFI Investor Education"
        }
        
    answer = gen_res.get("answer", "")
    citation = gen_res.get("citation_url", "")
    date_str = gen_res.get("last_updated", "July 2026")
    
    footer = f"Last updated from sources: {date_str}"
    
    return {
        "is_refused": False,
        "answer": answer,
        "citation_url": citation,
        "last_updated": date_str,
        "footer": footer,
        "scheme_referenced": gen_res.get("scheme_referenced", "")
    }
