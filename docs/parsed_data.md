# Ingested & Parsed Corpus Data Summary (`data/corpus.json`)

**Asset Management Company (AMC):** ICICI Prudential Mutual Fund  
**Reference Platform Context:** Groww  
**Regulatory Compliance Date:** July 2026  
**Total Ingested Schemes:** 5 Schemes  
**Total Semantic Knowledge Chunks:** 22 Verified Factual Chunks  

---

## 📊 Executive Comparative Summary Table (The 5 Covered Schemes)

The following matrix represents the factual parameters extracted directly from official Scheme Information Documents (SIDs), Key Information Memorandums (KIMs), and monthly factsheets corresponding to the 5 requested Groww URLs:

| Scheme Name | Category | Total Expense Ratio (TER) | Exit Load Policy | Minimum SIP | Riskometer Classification | Primary Benchmark Index | Official Groww URL |
| :--- | :--- | :---: | :--- | :---: | :---: | :--- | :--- |
| **ICICI Prudential Large Cap Fund** | Large Cap Fund | **0.88%** | 1.00% if redeemed $< 1$ year; Nil after 1 year | ₹100 / mo | Very High Risk | NIFTY 100 TRI | [Groww Link](https://groww.in/mutual-funds/icici-prudential-large-cap-fund-direct-growth) |
| **ICICI Prudential Dynamic Plan** | Dynamic Asset Allocation / BAF | **0.86%** | 1.00% on excess $> 30\%$ units within 1 yr; Nil after | ₹100 / mo | Very High Risk | CRISIL Hybrid 50+50 Moderate | [Groww Link](https://groww.in/mutual-funds/icici-prudential-dynamic-plan-direct-growth) |
| **ICICI Prudential Short Term Fund** | Short Duration Debt Fund | **0.38%** | **Nil (0.00%)** at all times; zero lock-in | ₹1,000 / mo | Moderate Risk | CRISIL Short Duration Debt A-II | [Groww Link](https://groww.in/mutual-funds/icici-prudential-short-term-plan-direct-growth) |
| **ICICI Prudential Flexicap Fund** | Flexi Cap Fund | **0.79%** | 1.00% if redeemed $< 12$ months; Nil after | ₹100 / mo | Very High Risk | S&P BSE 500 TRI | [Groww Link](https://groww.in/mutual-funds/icici-prudential-flexicap-fund-direct-growth) |
| **ICICI Prudential Top 100 Fund** | Large Cap Fund | **0.95%** | 1.00% if redeemed $< 1$ year; Nil after | ₹100 / mo | Very High Risk | NIFTY 100 TRI | [Groww Link](https://groww.in/mutual-funds/icici-prudential-top-100-fund-direct-growth) |

---

## 🏛️ General Regulatory & Investor Service Guidelines (All Schemes)

In addition to scheme-specific metrics, our ingestion pipeline parsed essential SEBI and AMFI regulatory rules that govern open-ended mutual fund investing:

| Regulatory Topic | Parsed Factual Rule | Statutory Authority / Source |
| :--- | :--- | :--- |
| **ELSS Statutory Lock-in** | Mandated **3-year (36 months) statutory lock-in** from date of allotment for tax-saving ELSS schemes under Section 80C. **Zero lock-in** applies to open-ended non-ELSS equity and debt schemes. | [AMFI ELSS Regulations](https://www.amfiindia.com/investor-corner/knowledge-center/elss.html) |
| **Account Statement & CAS Download** | Statement of Account (SoA) and Capital Gains reports downloadable via official AMC portal using Folio/PAN + OTP. Consolidated Account Statements (CAS) available via CAMS/AMFI portals. | [ICICI Pru AMC Services](https://www.icicipruamc.com/investor-services/statement-of-account) |
| **Public Document Accessibility** | Scheme Information Documents (SIDs), KIMs, and monthly factsheets are publicly downloadable without login mandates per SEBI transparency circulars. | [SEBI Document Circulars](https://www.sebi.gov.in/legal/circulars/mar-2024/simplification-and-rationalization-of-mutual-fund-scheme-information-document-_82337.html) |
| **Mutual Fund Taxation (FY 2024-26)**| Equity LTCG $> \text{₹}1.25\text{ lakh/yr}$ taxed at **12.5%** without indexation. Equity STCG ($< 12\text{ months}$ holding) taxed at a flat rate of **20%**. | [AMFI Taxation Guide](https://www.amfiindia.com/investor-corner/knowledge-center/taxation.html) |

---

## 🧩 Detailed Breakdown of the 22 Semantic Knowledge Chunks

Below is the complete inventory of semantic chunks parsed into `data/corpus.json`, categorized by scheme and topic. Each chunk is embedded using our local zero-cost `BAAI/bge-small-en-v1.5` neural vectorizer:

### 1. ICICI Prudential Large Cap Fund (Direct Plan - Growth)
* **`chunk_1` • Expense Ratio:** TER is approx. `0.88% per annum` as per official SIDs, representing the annual AMC management fee.
* **`chunk_2` • Exit Load:** `1.00% exit load` applicable if units are redeemed/switched within 1 year (365 days); `Nil exit load` after 1 year.
* **`chunk_3` • Minimum SIP & Lump Sum:** Minimum SIP is `Rs. 100/month` (multiples of Rs. 1 thereafter); minimum lump-sum initial investment is `Rs. 100`.
* **`chunk_4` • Lock-in Period:** Zero statutory lock-in period (open-ended equity scheme); investors can redeem on any business day.
* **`chunk_5` • Riskometer & Benchmark:** Classified as `'Very High Risk'`; benchmarked against `NIFTY 100 TRI`.

### 2. ICICI Prudential Dynamic Plan (Direct Plan - Growth)
* **`chunk_6` • Expense Ratio:** TER is approx. `0.86% per annum`; dynamically allocates across equity and debt instruments.
* **`chunk_7` • Exit Load:** `1.00% exit load` charged if units in excess of 30% of investment are redeemed within 1 year; `Nil exit load` for redemptions up to 30% within 1 year or any redemption after 1 year.
* **`chunk_8` • Minimum SIP & Lock-in:** Minimum SIP is `Rs. 100/month`; zero lock-in period.
* **`chunk_9` • Riskometer & Benchmark:** Classified as `'Very High Risk'`; benchmarked against `CRISIL Hybrid 50+50 - Moderate Index`.

### 3. ICICI Prudential Short Term Fund (Direct Plan - Growth)
* **`chunk_10` • Expense Ratio & Category:** TER is approx. `0.38% per annum`; open-ended short duration debt scheme with Macaulay duration between 1 and 3 years.
* **`chunk_11` • Exit Load & Lock-in:** `Nil (0.00%) exit load` at all times; zero lock-in period.
* **`chunk_12` • Minimum SIP & Benchmark:** Minimum SIP is `Rs. 1,000/month`; classified as `'Moderate Risk'`; benchmarked against `CRISIL Short Duration Debt A-II Index`.

### 4. ICICI Prudential Flexicap Fund (Direct Plan - Growth)
* **`chunk_13` • Expense Ratio & Overview:** TER is approx. `0.79% per annum`; dynamically invests across large-cap, mid-cap, and small-cap stocks.
* **`chunk_14` • Exit Load & Lock-in:** `1.00% exit load` if redeemed within 12 months; `Nil exit load` after 12 months; zero lock-in period.
* **`chunk_15` • Minimum SIP, Risk & Benchmark:** Minimum SIP is `Rs. 100/month`; classified as `'Very High Risk'`; benchmarked against `S&P BSE 500 TRI`.

### 5. ICICI Prudential Top 100 Fund (Direct Plan - Growth)
* **`chunk_16` • Expense Ratio & Overview:** TER is approx. `0.95% per annum`; predominantly invests in large-cap stocks representing the top 100 companies by market cap.
* **`chunk_17` • Exit Load & Lock-in:** `1.00% exit load` within 1 year; `Nil exit load` after 1 year; zero lock-in period.
* **`chunk_18` • Minimum SIP, Risk & Benchmark:** Minimum SIP is `Rs. 100/month`; classified as `'Very High Risk'`; benchmarked against `NIFTY 100 TRI`.

### 6. General Regulatory & AMFI Guidelines (All Schemes)
* **`chunk_19` • ELSS Lock-in Period:** Explains mandatory `3-year (36 months)` statutory lock-in for tax-saving ELSS funds vs zero lock-in for open-ended non-ELSS funds.
* **`chunk_20` • Statement Download:** Details procedure to download Statement of Account (SoA), Capital Gains statements, and Consolidated Account Statements (CAS) via CAMS/AMFI/AMC portals.
* **`chunk_21` • Official Public Sources:** Notes that SIDs, KIMs, and monthly factsheets are publicly accessible on the AMC website without login requirements.
* **`chunk_22` • Mutual Fund Taxation:** Outlines equity LTCG tax (`12.5%` above Rs. 1.25 lakh without indexation) and equity STCG tax (`20%` flat rate).
