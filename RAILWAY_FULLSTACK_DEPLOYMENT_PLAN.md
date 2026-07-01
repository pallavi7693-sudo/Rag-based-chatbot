# Unified Full-Stack Railway Deployment Plan (`FundIQ`)

> **Objective**: Deploy both the **Google Stitch Fintech Web UI** and the **FastAPI RAG Backend Engine** (including the daily automated ingestion scheduler) as a unified, high-performance application on **Railway Cloud**.

---

## 1. Executive Summary & Why Unified Railway Deployment?
Instead of hosting the frontend on Vercel and backend on Railway separately, deploying both on Railway under a single container service offers critical operational advantages:
- **Zero CORS Complexity**: Both UI and API reside on the same domain (`https://fundiq.up.railway.app`). Browser requests to `/api/chat` and `/api/schemes` execute instantly over same-origin HTTP/2 without preflight OPTIONS delays.
- **Unified Background Scheduling**: The asynchronous Daily Ingestion Scheduler (`src/backend/scheduler.py`) boots natively inside the container lifecycle, automatically refreshing Parquet datasets and RAM vector indexes every 24 hours.
- **Simpler Management**: Single git push deployment, centralized application logs, and simplified environment variable management.

---

## 2. Technical Architecture & Routing Matrix
Our application is pre-configured in `src/backend/app.py` to act as a unified full-stack web server:

| Path / Endpoint | Handler | Description |
| :--- | :--- | :--- |
| **`/`** | `serve_index()` | Serves `src/frontend/index.html` (Stitch Dark-Mode UI). |
| **`/styles.css`** | `serve_styles()` | Serves `src/frontend/styles.css` (Fintech visual styling). |
| **`/app.js`** | `serve_js()` | Serves `src/frontend/app.js` (`API_BASE_URL = ""`). |
| **`/api/chat`** | `chat_endpoint()` | POST endpoint executing Guardrails $\rightarrow$ BGE/TF-IDF RAG $\rightarrow$ Groq LLM. |
| **`/api/schemes`**| `schemes_endpoint()` | GET endpoint returning the 5 verified ICICI Prudential AMC schemes. |
| **`/health`** | `health_check()` | Live server heartbeat and API status check. |

---

## 3. Step-by-Step Railway Deployment Guide

### Step 1: Commit & Push to GitHub
Ensure all local changes (including your deleted Streamlit files and updated `requirements.txt`) are pushed to your GitHub repository:
```bash
git add .
git commit -m "Configure unified full-stack deployment for Railway"
git push origin main
```

### Step 2: Create Railway Service
1. Navigate to **[railway.app](https://railway.app)** and log in with your GitHub account.
2. Click **"New Project"** $\rightarrow$ **"Deploy from GitHub repo"**.
3. Select your **`RAG based chatbot`** repository.
4. Railway will automatically detect your project configuration:
   - **Runtime**: Python 3.11 (`runtime.txt`)
   - **Start Command**: `uvicorn src.backend.app:app --host 0.0.0.0 --port $PORT` (`Procfile`)

### Step 3: Configure Environment Secrets
1. In your Railway project dashboard, click on your deployed service card.
2. Navigate to the **"Variables"** tab.
3. Click **"New Variable"** and add your Groq API secret:
   ```text
   GROQ_API_KEY = your-groq-api-key-here
   ```
4. *Note*: Railway automatically injects the `$PORT` environment variable.

### Step 4: Generate Public Domain
1. In the Railway service dashboard, navigate to the **"Settings"** tab.
2. Under the **"Networking"** section, click **"Generate Domain"** (e.g., `https://fundiq-assistant.up.railway.app`).
3. Your application will trigger a fresh build and deploy!

---

## 4. Post-Deployment Verification Plan

Once your build shows **"Active"** on Railway, perform the following verification checks:

1. **Verify UI Loading**:
   - Open your generated Railway URL in any browser. Confirm the dark-mode Groww interface loads cleanly without missing stylesheets or logos.
2. **Test Factual RAG Generation**:
   - Click the sample question pill: *"What is the expense ratio of Large Cap fund?"*
   - Verify that the chat bubble returns a verified factual response within 3 sentences, displays the official SID citation badge, and appends the `Last updated: July 2026` timestamp.
3. **Test Advisory Refusal Guardrails**:
   - Type: *"Should I invest in this fund?"*
   - Confirm the system triggers an advisory refusal warning box and provides an AMFI Investor Education link.
4. **Verify Background Scheduler Logs**:
   - In the Railway **"Deployments"** -> **"View Logs"** console, confirm you see the daemon startup signature:
     ```text
     [SCHEDULER] [START] Daily Ingestion Daemon Started. Next cycle in 24.0 hours.
     ```
