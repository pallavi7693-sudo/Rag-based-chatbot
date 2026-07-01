# Stitch UI Generation Prompt: FundIQ (Facts-Only Mutual Fund Assistant)

> **Instructions**: Copy the prompt below and paste it directly into **Stitch** (Google's generative UI tool) to generate a premium, production-ready frontend web interface for your project!

---

## 📋 Copy-Paste Prompt for Stitch

```text
Create a modern, premium, and responsive web application UI for "FundIQ" — a SEBI-compliant, facts-only mutual fund FAQ assistant designed with the visual aesthetics of modern Indian fintech platforms like Groww (sleek typography, vibrant emerald green and indigo accents, glassmorphic card elements, and clean dark mode styling).

### 🎯 Core Purpose & Brand Identity
FundIQ helps retail investors and support teams get instant, verified answers about 5 ICICI Prudential mutual fund schemes (Large Cap, Dynamic, Short Term, Flexicap, Top 100) by retrieving data exclusively from official Scheme Information Documents (SIDs) and AMFI/SEBI guidance. The UI must instill trust, transparency, and institutional precision.

### 📐 Required Layout & UI Components

1. **Top Header & Navigation**:
   - Left: Brand Logo "FundIQ" with a subtle subtitle "Powered by Groww Knowledge Engine".
   - Center/Right: A glowing status pill saying "🟢 SEBI Compliant • Facts-Only RAG Engine", and an interactive button "📋 View Selected Schemes (5)".

2. **Hero & Welcome Section**:
   - Bold Headline: "Instant, Verified Mutual Fund Facts."
   - Subtitle: "Get verifiable answers on expense ratios, exit loads, SIP minimums, and tax statements directly from official AMC documents. Zero advisory bias."
   - Interactive Sample Question Chips (Clickable pills that auto-fill the chat):
     - 💡 "What is the expense ratio of Large Cap fund?"
     - 💡 "What is the minimum SIP for Top 100 fund?"
     - 💡 "How do I download my capital gains statement?"
     - 💡 "What is the exit load for Dynamic Plan?"

3. **Chat Conversation Area**:
   - A scrollable, well-spaced chat feed showing distinct message bubbles for the User and FundIQ.
   - **Assistant Response Bubble Structure**: Every answer card must visually enforce the SEBI regulatory format:
     - Main Answer Text (Clean typography, strictly <= 3 sentences).
     - Citation Badge: A sleek pill button with an external link icon saying "🔗 Official Source: Scheme Information Document (SID)".
     - Compliance Footer: Subtle muted text at the bottom right: "⏱️ Last updated from sources: July 2026".

4. **Special Visual States**:
   - **Typing / Retrieval Indicator**: An animated pulsing state showing: "🔍 Retrieving verified facts from official AMC/AMFI corpus..."
   - **Advisory Refusal Banner (Guardrail Triggered)**: If a user asks speculative questions like "Should I invest?" or "Which fund gives best returns?", render a distinct warning card with an amber/orange accent:
     - Icon: ⚠️
     - Title: "Advisory Query Detected"
     - Text: "FundIQ is a facts-only engine and strictly refuses investment advice or performance predictions. Please consult a SEBI-registered RIA or visit the AMFI Investor Education Center."
     - Clickable Link: "Explore AMFI Educational Guides ↗"

5. **Scheme Explorer Modal (Popup)**:
   - When clicking "View Selected Schemes (5)", open a clean modal displaying a table or grid of the 5 ICICI Prudential funds, their category (Large Cap, ELSS, Short Duration), Riskometer status (e.g., "Very High Risk" badge), and a link to their official SID.

6. **Bottom Sticky Input Bar & Persistent Disclaimer**:
   - Input field with placeholder: "Ask a factual question (e.g., exit load, SIP minimum, expense ratio)..."
   - Send Button with a send arrow icon and a clear button to reset chat.
   - **Mandatory Persistent Disclaimer Footer**: Fixed at the very bottom: "⚠️ SEBI Compliance Notice: Facts-only engine. No investment advice, return calculations, or portfolio recommendations are provided. Do not share personal data (PAN, OTP, bank account numbers)."

### 🎨 Design & Technical Specifications
- Use a refined dark palette (e.g., deep slate #0F172A background with emerald #10B981 and indigo #6366F1 gradient highlights) or an ultra-clean high-contrast white/gray fintech aesthetic.
- Ensure smooth micro-animations for message entry, hover effects on question chips, and modal opening.
- Generate modular HTML, TailwindCSS (or modern vanilla CSS), and clean Javascript ready to connect to a backend API endpoint (`POST /api/chat`).
```
