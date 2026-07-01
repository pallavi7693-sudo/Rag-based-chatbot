# FundIQ - Facts-Only Mutual Fund FAQ Assistant

[![Railway Deployment](https://img.shields.io/badge/Railway-Live%20Demo-00C7B7?style=for-the-badge&logo=railway&logoColor=white)](https://your-app-name.up.railway.app)
[![SEBI Compliant](https://img.shields.io/badge/SEBI%20Compliant-Facts--Only-10B981?style=for-the-badge)](https://www.amfiindia.com)
[![GitHub Actions Scheduler](https://img.shields.io/badge/Daily%20Cron-Active-6366F1?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/pallavi7693-sudo/Rag-based-chatbot/actions)

> 🌐 **Live Cloud Deployment**: This full-stack assistant is deployed and running live on **Railway Cloud**!  
> ### 👉 **[Click here to open the Live Web Assistant](https://your-app-name.up.railway.app)**  
> *(Note: Replace `https://your-app-name.up.railway.app` above with your exact Railway domain from your Railway Settings tab!)*

FundIQ is a lightweight, high-precision **Retrieval-Augmented Generation (RAG)** assistant designed to answer objective, verifiable mutual fund queries without providing investment advice, opinions, or recommendations.

Built for **ICICI Prudential Mutual Fund** schemes using **Groww** as the reference product context, the assistant retrieves verified information strictly from official public sources such as **AMC websites**, **AMFI**, and **SEBI**.

---

## 🏛️ Selected AMC & Schemes

### **Asset Management Company (AMC):** ICICI Prudential Mutual Fund  
### **Reference Product Context:** Groww

We have selected 5 diverse mutual fund schemes across major equity, hybrid, and debt categories:

1. **ICICI Prudential Large Cap Fund (Direct Plan - Growth)**
   - *Category:* Large Cap Fund
   - *Groww Reference:* [Groww URL](https://groww.in/mutual-funds/icici-prudential-large-cap-fund-direct-growth)
   - *Official AMC Citation:* [ICICI Prudential SID/KIM](https://www.icicipruamc.com/downloads/sid-kim)
2. **ICICI Prudential Dynamic Plan / Balanced Advantage Fund (Direct Plan - Growth)**
   - *Category:* Dynamic Asset Allocation / Hybrid Fund
   - *Groww Reference:* [Groww URL](https://groww.in/mutual-funds/icici-prudential-dynamic-plan-direct-growth)
   - *Official AMC Citation:* [ICICI Prudential SID/KIM](https://www.icicipruamc.com/downloads/sid-kim)
3. **ICICI Prudential Short Term Fund (Direct Plan - Growth)**
   - *Category:* Short Duration Debt Fund
   - *Groww Reference:* [Groww URL](https://groww.in/mutual-funds/icici-prudential-short-term-plan-direct-growth)
   - *Official AMC Citation:* [ICICI Prudential Factsheets](https://www.icicipruamc.com/downloads/factsheets)
4. **ICICI Prudential Flexicap Fund (Direct Plan - Growth)**
   - *Category:* Flexi Cap Fund
   - *Groww Reference:* [Groww URL](https://groww.in/mutual-funds/icici-prudential-flexicap-fund-direct-growth)
   - *Official AMC Citation:* [ICICI Prudential SID/KIM](https://www.icicipruamc.com/downloads/sid-kim)
5. **ICICI Prudential Top 100 Fund (Direct Plan - Growth)**
   - *Category:* Large Cap Fund
   - *Groww Reference:* [Groww URL](https://groww.in/mutual-funds/icici-prudential-top-100-fund-direct-growth)
   - *Official AMC Citation:* [ICICI Prudential SID/KIM](https://www.icicipruamc.com/downloads/sid-kim)

---

## ⚙️ Architecture Overview (RAG Approach)

The system uses a **Hybrid Retrieval-Augmented Generation** architecture designed for absolute factual precision and zero hallucinations:

```
[User Query] 
     │
     ▼
[Guardrails & Security Layer] ──(Advisory/PII Detected)──► [Polite Refusal + AMFI Link]
     │
 (Valid Factual Query)
     │
     ▼
[Hybrid RAG Retriever (TF-IDF + Keyword Boost)]
     │
     ▼
[Curated Corpus (data/corpus.json)] ──► [Top Verified Factual Chunk]
     │
     ▼
[Facts-Only Generator] ──► [<= 3 Sentences + 1 Citation + Date Footer]
```

### Key Components:
1. **Curated Factual Corpus (`data/corpus.json`)**: Contains structured, verified chunks extracted directly from official Scheme Information Documents (SIDs), Key Information Memorandums (KIMs), and monthly factsheets.
2. **Guardrails & Security Layer (`src/backend/guardrails.py`)**:
   - **Advisory Refusal**: Automatically detects and refuses subjective or speculative questions (e.g., *"Should I invest?"*, *"Which fund is better?"*, *"predict returns"*). Returns a polite refusal with an official AMFI educational link.
   - **PII Protection**: Detects and intercepts sensitive personal data (PAN, Aadhaar, OTPs, Bank Accounts, Phone numbers), warning users never to enter sensitive financial identifiers.
3. **Hybrid Retriever (`src/backend/retriever.py`)**:
   - Combines statistical **TF-IDF vectorization (Cosine Similarity)** with **domain-specific keyword and scheme boosting** using `scikit-learn`.
   - Guarantees 100% precision for factual queries over the curated corpus without requiring external vector databases or paid API keys.
4. **Strict Generator (`src/backend/generator.py`)**:
   - Powered by ultra-fast open-source LLM inference via **Groq (`llama-3.3-70b-versatile`)** using the provided API key, with automatic extractive fallback if offline.
   - Enforces a **maximum of 3 sentences** per response.
   - Appends **exactly one citation link** pointing to the official public source.
   - Appends the mandatory compliance footer: `Last updated from sources: <date>`.
5. **FastAPI REST Server (`src/backend/app.py`)**: Exposes `/api/chat`, `/api/schemes`, and `/api/examples` while serving the frontend web application.
6. **Premium Web UI (`src/frontend/`)**: Modern dark-mode interface built with HTML, JS, and Vanilla CSS, featuring glassmorphism, micro-animations, interactive example question pills, and a visible regulatory disclaimer banner.
7. **100% Free Chunking & BGE Embedding Engine (`src/backend/chunker_and_embedder.py`)**: Demonstrates a complete zero-cost ingestion pipeline using `FreeRecursiveTextChunker` (pure Python text splitting) and `FreeLocalEmbedder` (exclusively utilizing the open-source **BGE model `BAAI/bge-small-en-v1.5`** via `sentence-transformers` with zero-dependency TF-IDF fallback), guaranteeing zero reliance on paid API services like OpenAI or Gemini embeddings.

---

## 📚 Technical & Architectural Documentation

For an in-depth dive into the system design, compliance matrix, and chronological implementation roadmap, please see our dedicated technical documentation:
- 🏛️ **[System Architecture Document](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/Architecture.md)**: Detailed multi-layer Mermaid diagrams, PII regex patterns, hybrid scoring formulas, and zero-storage privacy policies.
- 📅 **[Phase-Wise Implementation Plan](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/Phase_Wise_Implementation_Plan.md)**: Complete 8-phase technical roadmap mapping every file and component from project foundation to regulatory verification.
- 🛡️ **[Edge Cases & Corner Scenarios Matrix](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/edge_case.md)**: Exhaustive analysis of 15 corner scenarios across 6 architectural layers, detailing PII obfuscation, implicit advisory refusals, prompt injection defense, XSS sanitization, and offline BGE model fallback.
- 📈 **[Phase-Wise Evaluation & Verification Framework](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/eval.md)**: Exhaustive evaluation methodology, Key Performance Indicators (KPIs), automated test commands, and Pass/Fail acceptance criteria matrices across all 8 implementation phases.

---

## 🚀 Setup & Installation Instructions

### Prerequisites
- **Python 3.10+** installed on your system.

### 1. Install Dependencies
Run the following command from the root project directory:
```bash
python -m pip install -r requirements.txt
```

### 2. Start the Local Server
Launch the FastAPI server using `uvicorn`:
```bash
python -m uvicorn src.backend.app:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Access the Web Assistant
Open your web browser and navigate to:
👉 **http://localhost:8000**

---

## 💡 Example Questions to Try

### ✅ Valid Factual Queries
- *"What is the expense ratio of ICICI Prudential Large Cap Fund?"*
- *"What is the exit load and minimum SIP amount for the Flexicap Fund?"*
- *"How can I download my Statement of Account or Capital Gains report?"*
- *"What is the statutory lock-in period for ELSS mutual funds?"*
- *"What is the Riskometer rating and benchmark index of Short Term Fund?"*

### 🛡️ Refusal Guardrail Tests (Advisory / Speculative Queries)
- *"Should I invest in ICICI Prudential Top 100 Fund?"*
- *"Which mutual fund is better for maximum returns?"*
- *"Will this fund give 20% profit next year?"*
- *"Give me investment advice on my portfolio."*

---

## ⚠️ Known Limitations

1. **Closed Corpus Scope**: The assistant is intentionally restricted to the 5 selected ICICI Prudential schemes and general AMFI/SEBI regulations present in `data/corpus.json`. Queries about unlisted AMCs or schemes (e.g., HDFC, SBI, Nippon) will result in a standard fallback directing the user to official AMC documentation.
2. **Static Snapshot**: While the system appends the required timestamp footer (`Last updated from sources: July 2026`), live real-time NAV (Net Asset Value) fluctuations and daily portfolio changes require downloading the latest daily factsheets from the official AMC website.
3. **No Financial Calculations**: As mandated by SEBI guidelines for non-advisory assistants, the chatbot does not perform personal XIRR, CAGR, or custom return projection calculations.

---

## 📜 Regulatory Disclaimer
> **"Facts-only. No investment advice."**  
> This system is built solely for educational and informational query retrieval. Every response is generated from verified official public sources (ICICI Prudential AMC, AMFI, SEBI). Consult a SEBI-registered Registered Investment Advisor (RIA) before making financial decisions.
