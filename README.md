# 🛡️ Zero-Trust Access Proxy with Continuous Risk Scoring Engine
### Autonomous Behavioral Telemetry & Adaptive SIEM Micro-Segmentation System

An enterprise-grade cybersecurity and big data stream-processing pipeline engineered to eliminate implicit trust in active sessions under the Zero-Trust doctrine: **"Never Trust, Always Verify"**.

---

## 📌 Project Overview
* **Domain:** Big Data Distributed Streaming, Machine Learning & Cybersecurity
* **Syllabus Mapping:** 
  * Big Data Technologies Elective Practical (`NTITEL5P1`)
  * Information Systems Security (`NTITMJ503`)
* **Student Name:** PANKAJ SURENDRA VARMA
* **Roll Number:** 19061
* **Institution:** S.I.W.S. College of Commerce & Economics and Smt. Thirumalai College of Science
* **Guide:** Prof. Aditya Rathod

---

## ⚙️ Key Architecture & Features
1. **Decoupled Stream Ingestion:** In-memory asynchronous FIFO broker simulating Apache Kafka topics to buffer high-velocity HTTP access telemetry without blocking client responses.
2. **Behavioral Feature Engineering:** Real-time extraction of multivariate vectors across sliding windows: `[Payload Size (KB), Arrival Delta (s), Route Sensitivity Flag]`.
3. **Unsupervised ML Anomaly Scoring:** Uses an `IsolationForest` estimator coupled with dynamic threat heuristic weights to produce a continuous risk index ($0$ to $100$).
4. **Three-Tier Adaptive Enforcement:**
   * **Score < 45:** Verified Access Granted (`ALLOW_REQUEST`)
   * **Score 45 - 74:** Step-Up Verification Prompt (`REQUIRE_STEPUP_MFA`)
   * **Score ≥ 75:** Immediate Session Isolation & IP Block (`TERMINATE_SESSION_BLOCK_IP`)
5. **NoSQL State & Audit Store:** Structured document datastore (`zero_trust_datastore.json`) preserving live identity registries and immutable security audit trails.
6. **Executive SOC Command Center:** Modern dark-theme dashboard built with Streamlit and Plotly, featuring real-time polling, live anomaly trendlines, and manual exploit injection sandboxing.

---

## 📊 Live Telemetry Benchmarks
* **Total Processed Packets:** 179+ Requests
* **Access Granted (Baseline Traffic):** 107 Requests (Risk: 10–25/100)
* **MFA Step-Up Challenges:** 3 Occurrences (Risk: 45–70/100)
* **Threats Blocked & Quarantined:** 69 Malicious Bursts (Risk: 85–100/100)
* **Quarantined Identities:** 2 Rogue Nodes

---

## 🚀 How to Run Locally

### 1. Install Dependencies
```bash
pip install streamlit plotly scikit-learn pandas numpy