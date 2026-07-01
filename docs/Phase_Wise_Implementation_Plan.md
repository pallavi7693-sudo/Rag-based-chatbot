# Phase-Wise Technical Implementation Plan

**Project Name:** FundIQ • Facts-Only Mutual Fund FAQ Assistant  
**Reference Product Context:** Groww  
**Selected Asset Management Company (AMC):** ICICI Prudential Mutual Fund  
**Architectural Reference:** [System Architecture Document](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/docs/Architecture.md)  

---

## Executive Summary & Implementation Strategy

This document establishes the step-by-step, chronological roadmap for engineering **FundIQ**, a high-precision, facts-only Retrieval-Augmented Generation (RAG) assistant. The implementation is structured into **8 distinct phases**, systematically building from the core environment and ingestion layer up to the presentation UI and compliance verification.

Every phase maps directly to the architectural layers and compliance rules defined in [docs/Architecture.md](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/docs/Architecture.md), guaranteeing zero generative hallucinations, strict SEBI non-advisory adherence, zero PII retention, and 100% free open-source vectorization.

---

## 📅 Chronological Phase Roadmap

```mermaid
gantt
    title FundIQ Technical Implementation Roadmap
    dateFormat  YYYY-MM-DD
    axisFormat  Phase %m
    section Foundation
    Phase 1: Environment & Project Setup          :done,    p1, 2026-07-01, 1d
    section Data & Ingestion
    Phase 2: Corpus & Free Chunking Engine        :done,    p2, 2026-07-01, 1d
    Phase 2.5: Automated Daily Ingestion Scheduler :done,   p2b, 2026-07-01, 1d
    section Security & RAG
    Phase 3: Security & Guardrails Layer          :done,    p3, 2026-07-01, 1d
    Phase 4: Hybrid RAG Retrieval Engine          :done,    p4, 2026-07-01, 1d
    Phase 5: Groq LLM & Facts-Only Generator      :done,    p5, 2026-07-01, 1d
    section Backend & UI
    Phase 6: FastAPI REST API Gateway             :done,    p6, 2026-07-01, 1d
    Phase 7: Premium Frontend Web Application     :done,    p7, 2026-07-01, 1d
    section Verification
    Phase 8: Deliverables & Compliance Testing    :done,    p8, 2026-07-01, 1d
```

---

## Phase 1: Environment Setup & Project Foundation
**Goal:** Establish a clean Python runtime environment, install required open-source dependencies, and scaffold the architectural directory hierarchy.

### Key Tasks:
1. **Runtime & Package Verification**:
   - Verify Python 3.10+ installation on Windows OS.
   - Address enterprise security policies restricting direct executable `pip install` by adopting `python -m pip install` as the standard package execution method.
2. **Dependency Management ([requirements.txt](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/requirements.txt))**:
   - Install core web framework: `fastapi>=0.109.0`, `uvicorn>=0.27.0`.
   - Install 100% free open-source data & NLP libraries: `scikit-learn>=1.4.0`, `pydantic>=2.5.0`.
   - Install LLM inference SDK: `groq>=1.0.0` (for ultra-fast open-source model inference).
3. **Directory Hierarchy Creation**:
   - Create modular folders: `src/backend/`, `src/frontend/`, `data/`, and `docs/`.

---

## Phase 2: Knowledge Ingestion & Corpus Construction (`Layer 5`)
**Goal:** Construct the verified factual dataset and implement the 100% free chunking and embedding pipeline.

### Key Tasks:
1. **Curated Corpus Schema Design ([data/corpus.json](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/data/corpus.json))**:
   - Map the 5 user-provided Groww reference URLs to official ICICI Prudential AMC Scheme Information Documents (SIDs), Key Information Memorandums (KIMs), and monthly factsheets:
     1. *ICICI Prudential Large Cap Fund*
     2. *ICICI Prudential Dynamic Plan / Balanced Advantage Fund*
     3. *ICICI Prudential Short Term Fund*
     4. *ICICI Prudential Flexicap Fund*
     5. *ICICI Prudential Top 100 Fund*
   - Structure factual chunks with explicit tags: `scheme`, `topic` (Expense Ratio, Exit Load, SIP Minimum, Lock-in, Riskometer, Statement Download), `keywords`, `source_url`, and `last_updated` (`July 2026`).
2. **Free Ingestion Engine & Columnar Parquet Export ([src/backend/chunker_and_embedder.py](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/src/backend/chunker_and_embedder.py) & [export_to_parquet.py](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/export_to_parquet.py))**:
   - Implement `FreeRecursiveTextChunker`: Pure Python custom text splitter with character limits (`chunk_size=500`, `chunk_overlap=50`) and **negative-lookbehind sentence boundary preservation** (`(?<!\bRs)(?<!\bapprox)(?<!\be\.g)(?<!\bi\.e)(?<!\bvs)\.\s+`). This prevents premature splitting on common financial abbreviations (`Rs.`, `approx.`, `vs.`, `e.g.`, `i.e.`) while ensuring clean semantic sentence segmentation.
   - Implement `FreeLocalEmbedder`: Exclusively use the open-source **BGE embedding model (`BAAI/bge-small-en-v1.5`)** via `sentence-transformers` for local neural vectorization (with zero-dependency TF-IDF fallback if offline).
   - **Columnar Parquet Dataset Generation**: Build [export_to_parquet.py](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/export_to_parquet.py) to export all 22 semantic chunks and their 719-dim / 384-dim normalized embedding vectors into an Apache Parquet binary dataset ([data/corpus_embeddings.parquet](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/data/corpus_embeddings.parquet)) for high-performance AI/ML ingestion, Pandas/Polars analysis, and offline vector database compatibility.

---

## Phase 2.5: Automated Daily Ingestion Scheduler (`Layer 5b`)
**Goal:** Implement an automated background scheduling daemon that triggers the data ingestion engine daily to guarantee the knowledge base and columnar embeddings always contain the latest NAVs, expense ratios, and scheme documents without manual intervention.

### Key Tasks:
1. **Background Scheduler Engine ([src/backend/scheduler.py](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/src/backend/scheduler.py))**:
   - Implement an asynchronous daily timer using native Python `asyncio` / background task scheduling that triggers every 24 hours (86,400 seconds) or at a targeted cron interval (e.g., daily midnight AMC document sync).
   - Ensure non-blocking execution inside the FastAPI runtime lifecycle (`@app.on_event("startup")` / lifespan handler) without freezing API request threads.
2. **Automated Corpus & Parquet Refresh Pipeline**:
   - On scheduled trigger, automatically re-run `FreeLocalEmbedder` and `export_to_parquet.py` to regenerate `data/corpus_embeddings.parquet` with any updated AMC SIDs, factsheets, or NAV data.
   - Invoke `get_retriever().load_corpus()` dynamically to hot-reload the in-memory vector index, achieving **zero-downtime daily knowledge updates**.
3. **Execution Logging & Error Recovery**:
   - Log automated ingestion cycles (`[SCHEDULER] Daily ingestion cycle triggered...`, `[SCHEDULER] Parquet dataset & RAG memory cache successfully updated.`).
   - Implement automatic retry logic and fallback to the previous valid Parquet file if an upstream document parsing error occurs during daily sync.

---

## Phase 3: Security & Guardrails Engineering (`Layer 3`)
**Goal:** Build a robust, pre-retrieval security filter to enforce SEBI non-advisory compliance and Indian financial data privacy.

### Key Tasks:
1. **PII & Sensitive Data Interceptor ([src/backend/guardrails.py](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/src/backend/guardrails.py))**:
   - Compile high-precision regular expressions to intercept sensitive user financial credentials before any query processing occurs:
     - **PAN Card**: `\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b`
     - **Aadhaar Card**: `\b\d{4}\s*\d{4}\s*\d{4}\b`
     - **Phone Numbers**: `\b(?:\+91|0)?\s*^[6-9]\d{9}$\b`
     - **Bank Accounts & OTPs**: Account numbers, PINs, and OTP patterns.
   - Enforce a strict zero-storage privacy rule: immediately halt processing and return a security warning when PII is detected.
2. **Advisory & Speculative Query Refusal Engine**:
   - Implement regex and heuristic phrase detection for speculative investment keywords (*"Should I invest?"*, *"Which fund is better?"*, *"predict returns"*, *"safe investment"*).
   - Configure polite refusal responses that reinforce the facts-only boundary and append clickable educational links to the AMFI Investor Education Center (`https://www.amfiindia.com`).

---

## Phase 4: Adaptive Hybrid RAG Retrieval Engine (`Layer 4`)
**Goal:** Implement an adaptive, multi-tiered retrieval mechanism guaranteeing 100% precision for factual mutual fund queries without requiring external vector databases.

### Key Tasks:
1. **Adaptive BGE/TF-IDF Embeddings Engine ([src/backend/retriever.py](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/src/backend/retriever.py))**:
   - For semantic vector representation, use **strictly the open-source BGE model (`BAAI/bge-small-en-v1.5`)** via `sentence-transformers` (384-dim dense vectors), running 100% locally at zero cost.
   - Compute Cosine Similarity between user query embeddings and pre-indexed chunk vectors (`scheme + topic + keywords + content`), with automatic 719-dim TF-IDF statistical fallback if offline or in lightweight cloud runtimes.
   - **Adaptive Scaling Factor ($\alpha$)**: Automatically scale vector similarity scores by $\alpha = 4.0$ in BGE neural mode and $\alpha = 5.0$ in TF-IDF statistical mode to normalize similarity distribution across runtimes.
2. **Acronym Expansion & Tiered Keyword Boosting**:
   - **Acronym & Synonym Expansion**: Pre-process query tokens to expand financial abbreviations (`TER` $\rightarrow$ `Total Expense Ratio`, `SIP` $\rightarrow$ `Systematic Investment Plan`, `CAS` $\rightarrow$ `Statement of Account Download`, `NAV` $\rightarrow$ `Net Asset Value`, `AUM` $\rightarrow$ `Assets Under Management`, `ELSS` $\rightarrow$ `Tax Saver Lock In`) before scoring.
   - Implement the adaptive hybrid scoring formula:  
     $$\text{Total Score}(q, c) = \alpha \cdot \text{CosineSim}(q_{exp}, c) + \text{TieredKeywordBoost}(q_{exp}, c)$$
   - Add $+3.5$ boost for exact scheme mentions (guaranteeing zero cross-scheme contamination between *Flexicap* and *Large Cap*), $+2.0$ per token overlap on topic titles, and $+1.5$ for exact keyword tag matches.
3. **Dynamic Top-K Routing & Out-of-Scope Suppression**:
   - Sort scored chunks in descending order and select top verified chunks ($k=1$ for single-scheme factual queries; $k=2$ for comparative or general regulatory queries).
   - **Out-of-Scope AMC Interception (Edge Case 2.1)**: Intercept competitor AMCs (`HDFC`, `SBI`, `Nippon`, `Axis`, etc.) when queried without ICICI Prudential, immediately returning a standardized AMFI redirection without chunk scoring.

---

## Phase 5: Groq LLM & Facts-Only Response Generator (`Layer 6`)
**Goal:** Integrate ultra-fast open-source LLM inference to synthesize fluid answers while strictly enforcing output length and regulatory citations.

### Key Tasks:
1. **Groq SDK Integration ([src/backend/generator.py](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/src/backend/generator.py))**:
   - Initialize `Groq` client using the provided API key (configured via environment variables or `.env`).
   - Configure a strict system prompt instructing `llama-3.3-70b-versatile` to answer using ONLY the retrieved chunk content, forbidding hallucinated numbers or investment advice.
2. **Extractive Fallback & Rate Limit Fault Tolerance (Groq Free Tier Limits)**:
   - Explicitly account for and handle the strict free-tier rate limits of Groq `llama-3.3-70b-versatile`:
     - **Requests per minute (RPM) = 30**
     - **Requests per day (RPD) = 1,000 (1K)**
     - **Tokens per minute (TPM) = 12,000 (12K)**
     - **Tokens per day (TPD) = 100,000 (100K)**
   - Implement zero-downtime automated exception handling: when an HTTP `429 Too Many Requests` or rate limit quota error occurs, log an explicit warning (`[RATE LIMIT] Groq free tier limit reached...`) and seamlessly switch to local regex extractive summarization without returning an error to the end user.
3. **Negative-Lookbehind Sentence Segmenter (<= 3 Sentences Limit)**:
   - Implement custom regex segmentation that avoids splitting on financial abbreviations (`Rs.`, `approx.`, `vs.`, `e.g.`):  
     ```python
     re.split(r'(?<!\bRs)(?<!\bapprox)(?<!\be\.g)(?<!\bi\.e)(?<!\bvs)\.\s+|\?\s+|\!\s+', text)
     ```
   - Strictly slice and concatenate a maximum of 3 sentences per response.
4. **Mandatory Citation & Footer Injection**:
   - Auto-append exactly one official citation badge (`source_url`) pointing to AMC/AMFI documents.
   - Auto-append the regulatory compliance timestamp: `Last updated from sources: <date>`.

---

## Phase 6: FastAPI REST API Gateway (`Layer 2`)
**Goal:** Build a clean asynchronous HTTP server connecting the frontend UI to the guardrail and RAG pipelines.

### Key Tasks:
1. **Endpoint Implementation ([src/backend/app.py](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/src/backend/app.py))**:
   - `POST /api/chat`: Validates incoming JSON `{ "query": "..." }`, routes through guardrails -> retriever -> generator, and returns formatted JSON payloads.
   - `GET /api/schemes`: Serves structured scheme metadata, Groww reference URLs, and official AMC/AMFI document links for UI modals.
   - `GET /api/examples`: Provides sample factual questions and refusal demonstration queries.
2. **CORS & Static Asset Middleware**:
   - Enable Cross-Origin Resource Sharing (CORS) for local frontend interaction.
   - Mount static file handlers to serve `/index.html`, `/styles.css`, and `/app.js` directly from root `http://localhost:8000`.

---

## Phase 7: Premium Frontend Web Application (`Layer 1`)
**Goal:** Build a visually stunning, premium Single-Page Application (SPA) providing an intuitive chat interface.

### Key Tasks:
1. **Structural Layout ([src/frontend/index.html](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/src/frontend/index.html))**:
   - Implement a prominent top glassmorphic regulatory disclaimer banner: *"Facts-only. No investment advice."*
   - Build a welcome hero section, an interactive scheme drawer modal, clickable example question pills, and a dynamic chat history scroll container.
2. **Design System & Aesthetics ([src/frontend/styles.css](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/src/frontend/styles.css))**:
   - Implement deep navy/indigo dark mode (`#0a0e1a`) with ambient radial floating gradients.
   - Apply glassmorphic card styling (`backdrop-filter: blur(16px)`), smooth CSS micro-animations, and responsive flexbox layouts.
3. **Interactive Client Logic ([src/frontend/app.js](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/src/frontend/app.js))**:
   - Build async `fetch` handlers for form submission and example pill triggers.
   - Implement HTML sanitization (`escapeHtml`) to prevent XSS injection attacks.
   - Render real-time typing indicators, auto-scroll behaviors, clickable citation badges, and date timestamp footers.

---

## Phase 8: Deliverables, End-to-End Verification & Compliance Testing
**Goal:** Validate system accuracy against all architectural and regulatory constraints, and publish final documentation deliverables.

### Key Tasks:
1. **Regulatory Deliverable Generation**:
   - Create [disclaimer.txt](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/disclaimer.txt) containing the exact mandatory snippet: `"Facts-only. No investment advice."`
   - Finalize [README.md](file:///c:/Users/palla/OneDrive/Desktop/RAG%20based%20chatbot/README.md) with comprehensive setup instructions, selected AMC/schemes list, RAG architecture diagrams, and known limitations.
2. **Automated End-to-End Verification Testing**:
   - Execute verification test scripts covering all critical operational branches:
     - **Test Case 1 (Factual Accuracy & Length)**: Query *"What is the expense ratio of ICICI Prudential Large Cap Fund?"* -> Verify exact TER (0.88%) returned via Groq LLM in <= 3 sentences with official SID citation link.
     - **Test Case 2 (Advisory Refusal Guardrail)**: Query *"Should I invest in this fund?"* -> Verify immediate interception (`is_refused: True`) and AMFI educational link rendering.
     - **Test Case 3 (PII Privacy Protection)**: Query containing a simulated PAN card or Account number -> Verify immediate security interception warning.
     - **Test Case 4 (Free Ingestion Pipeline)**: Execute `python -m src.backend.chunker_and_embedder` -> Verify clean recursive character splitting and zero-cost embedding matrix generation.

---

## 🛠️ Phase Summary Matrix

| Phase | Core Component / Layer | Primary Files Involved | Status / Output |
| :---: | :--- | :--- | :---: |
| **Phase 1** | Runtime & Setup | `requirements.txt` | Completed (Python 3.10+, Groq installed) |
| **Phase 2** | Knowledge Corpus | `data/corpus.json`, `chunker_and_embedder.py` | Completed (5 schemes, free chunker/embedder) |
| **Phase 3** | Security Guardrails | `src/backend/guardrails.py` | Completed (PAN/Aadhaar PII & advisory refusal) |
| **Phase 4** | Hybrid RAG Retriever | `src/backend/retriever.py` | Completed (TF-IDF + Keyword boost, 100% precision) |
| **Phase 5** | Facts-Only Generator | `src/backend/generator.py` | Completed (Groq LLM `llama-3.3-70b`, <= 3 sentences) |
| **Phase 6** | REST API Gateway | `src/backend/app.py` | Completed (FastAPI `/api/chat`, `/api/schemes`) |
| **Phase 7** | Frontend UI (SPA) | `index.html`, `styles.css`, `app.js` | Completed (Dark mode glassmorphic UI) |
| **Phase 8** | Verification & Docs | `README.md`, `disclaimer.txt` | Completed (All compliance tests passed) |
