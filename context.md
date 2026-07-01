# FundIQ: Project Context & Architectural Constitution (`context.md`)

> **Note for AI Coding Assistants & Developers**: This file is the authoritative technical briefing and domain constitution for the **FundIQ** project. Always reference the constraints, architectural layers, and SEBI regulatory rules defined below before making code or documentation changes.

---

## 1. Project Mission & Core Domain
**FundIQ** is a lightweight, high-precision **Retrieval-Augmented Generation (RAG)** FAQ assistant designed to answer factual mutual fund queries using **Groww** as the product design reference.
- **Exclusivity**: Retrieves verifiable objective facts strictly from official **ICICI Prudential Asset Management Company (AMC)** documents (SIDs, KIMs, Factsheets) and regulatory bodies (**AMFI / SEBI**).
- **Core Philosophy**: *Accuracy over intelligence.* The system strictly refuses advisory opinions, performance predictions, and portfolio recommendations.

---

## 2. Technology Stack & Runtime Specifications

### 🐍 Backend Infrastructure (Python 3.11+)
- **API Gateway**: **FastAPI** (`src/backend/app.py`) running asynchronous REST endpoints with full CORS middleware enabled for cross-origin cloud requests.
- **LLM Inference**: **Groq Cloud SDK** (`src/backend/generator.py`) running `llama-3.3-70b-versatile` at deterministic zero temperature (`temperature=0.0`).
- **Embedding & Chunking Engine**: **Sentence-Transformers** (`src/backend/chunker_and_embedder.py`) running the open-source BGE neural model (`BAAI/bge-small-en-v1.5`, 384-dim). Includes an automated fallback to statistical **TF-IDF Vocabulary Vectorization** (~719-dim) for offline or lightweight serverless environments.
- **Data Science & Storage**: 
  - Factual JSON Corpus: `data/corpus.json` (22 verified semantic chunks across 5 ICICI Prudential schemes).
  - Columnar AI Dataset: `data/corpus_embeddings.parquet` (Generated via `export_to_parquet.py` using Apache Arrow/PyArrow).

### 🌐 Frontend Web Interface (Vanilla HTML5 / JS / CSS3)
- **Zero-Dependency SPA**: Built with native browser APIs (`src/frontend/index.html`, `app.js`, `styles.css`) for instant loading and maximum compatibility.
- **Dynamic Cloud Routing**: Configured with `API_BASE_URL` in Javascript and `vercel.json` rewrites for seamless proxying between Vercel and Railway.

### ☁️ Cloud Deployment Setup
- **Backend**: Pre-configured for **Railway** via `Procfile`, `runtime.txt`, and `railway.json`.
- **Frontend**: Pre-configured for **Vercel** static hosting with `/api/*` reverse-proxying.

---

## 3. Mandatory SEBI Regulatory Guardrails & Constraints
Any code modification **MUST** preserve the following four inviolable guardrails:

1. **The 3-Sentence Limit**:
   - Every AI response must be strictly capped at a **maximum of 3 sentences**.
   - Enforced by regex negative-lookbehind segmentation (`(?<!\bRs)(?<!\bapprox)(?<!\be\.g)(?<!\bi\.e)(?<!\bvs)\.\s+`) to prevent premature splitting on financial abbreviations (`Rs.`, `approx.`, `vs.`, `e.g.`).
2. **Single Citation Mandate**:
   - Every response must include **exactly one clickable source link** (`source_url`) pointing to an official AMC SID or AMFI educational page.
3. **Mandatory Compliance Footer**:
   - Every answer must append the exact timestamp badge:  
     `Last updated from sources: July 2026` (or current corpus date).
4. **Advisory & PII Interception**:
   - **No Investment Advice**: Automatically intercept and politely refuse speculative queries (*"Should I invest?"*, *"Which fund is best?"*) and provide a link to AMFI Investor Education.
   - **Zero PII Storage**: Immediately block and drop any user input containing Permanent Account Numbers (PAN), Aadhaar, Bank Accounts, PINs, or OTPs.

---

## 4. Adaptive Hybrid Retrieval Strategy (`Layer 4`)
The retrieval engine (`src/backend/retriever.py`) uses a dual-engine reciprocal scoring formula:
$$\text{Total Score}(q, c) = \alpha \cdot \text{CosineSim}(q_{exp}, c) + \text{TieredKeywordBoost}(q_{exp}, c)$$

- **Adaptive Scaling ($\alpha$)**: $\alpha = 4.0$ when running in neural BGE mode (384-dim) and $\alpha = 5.0$ when running in statistical TF-IDF mode (719-dim).
- **Acronym & Synonym Expansion**: Auto-expands financial terms before scoring (`TER` $\rightarrow$ `Expense Ratio`, `SIP` $\rightarrow$ `Systematic Investment Plan`, `CAS` $\rightarrow$ `Statement of Account`, `NAV` $\rightarrow$ `Net Asset Value`, `AUM` $\rightarrow$ `Assets Under Management`).
- **Tiered Domain Boosting**: $+3.5$ for exact scheme name matches, $+2.0$ per token overlap on topic titles, and $+1.5$ for keyword tag hits.
- **Dynamic $K$-Routing**: Returns top $k=1$ chunk for single-scheme factual queries and $k=2$ for multi-scheme comparisons or general taxation rules.
- **Out-of-Scope AMC Interception**: Queries mentioning competitor AMCs (`HDFC`, `SBI`, `Nippon`, `Axis`, etc.) without ICICI Prudential are intercepted immediately with an AMFI redirection.

---

## 5. Directory & File Mapping
```text
RAG based chatbot/
├── data/
│   ├── corpus.json                 # Core verified factual knowledge base (22 chunks)
│   └── corpus_embeddings.parquet   # Columnar data science dataset with vectors
├── docs/
│   ├── Architecture.md             # System design & layer specifications
│   ├── Phase_Wise_Implementation_Plan.md # Implementation roadmap
│   ├── problemstatement.md         # Original project objective & scope
│   └── STITCH_UI_PROMPT.md         # Generative AI UI builder prompt
├── src/
│   ├── backend/
│   │   ├── app.py                  # FastAPI REST API server
│   │   ├── chunker_and_embedder.py # FreeLocalEmbedder & Recursive chunker
│   │   ├── guardrails.py           # PII filter & advisory refusal engine
│   │   ├── retriever.py            # Adaptive Hybrid RAG search engine
│   │   └── generator.py            # Groq LLM inference & rate-limit fallback
│   └── frontend/
│       ├── index.html              # Vanilla SPA structure & disclaimers
│       ├── app.js                  # Chat UI logic & API Base URL routing
│       └── styles.css              # Dark/light fintech visual styles
├── DEPLOYMENT_GUIDE.md             # Step-by-step Railway & Vercel guide
├── export_to_parquet.py            # Dataset generation script
├── Procfile / railway.json         # Railway cloud backend configuration
├── vercel.json                     # Vercel cloud frontend rewrite rules
└── requirements.txt                # Python project dependencies
```

---

## 6. Quick Start & CLI Commands
- **Run API Backend Locally**:
  ```bash
  uvicorn src.backend.app:app --host 0.0.0.0 --port 8000 --reload
  ```
- **Test Retrieval & Acronym Expansion**:
  ```bash
  python -c "from src.backend.retriever import retrieve_facts; print(retrieve_facts('ter large cap')[0]['scheme'])"
  ```
- **Regenerate Apache Parquet Dataset**:
  ```bash
  python export_to_parquet.py
  ```
