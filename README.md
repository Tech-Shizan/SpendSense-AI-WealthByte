<div align="center">

# 💸 SpendSense AI

**Intelligent, Privacy-First Personal Finance & Smart Budgeting Assistant**

Developed by Team **WealthByte**

---

</div>

## 📌 Overview

**SpendSense AI** is an intelligent, privacy-first personal finance and budgeting assistant that uses local Regex PII masking before sending data to Google Gemini LLM. Includes automatic fallback routing and MongoDB chat history.

With financial data privacy as a core tenet, sensitive identifiers such as credit/debit card numbers, bank account numbers, phone numbers, and email addresses are automatically sanitized client-side before any prompt reaches the AI model or database.

---

## ✨ Key Features

- **🛡️ Privacy-First Architecture (Local PII Sanitization):**
  Uses high-performance regex masks client-side to strip card/account numbers (13–19 digits), phone numbers, and email addresses before external API transmission.
- **🧠 Dual-Model LLM Intelligence with Auto-Fallback:**
  Powered by Google Gemini via LangChain LCEL pipelines (`gemini-3.5-flash`), with automatic error catching and seamless fallback to `gemini-3.5-flash-lite` during high-demand or quota scenarios.
- **🧾 Bill & Receipt Analysis:**
  Extracts items, classifies expenses into categories (Food, Grocery, Transport, Healthcare, Shopping, Bills, Other), verifies totals, and spots discrepancies.
- **💡 Actionable Budgeting Insights:**
  Delivers tailored recommendations based on user income and spending trends without assuming unverified currency units.
- **🗄️ Persistent MongoDB Chat History:**
  Stores anonymized conversation sessions, allows pinning priority chats, and maintains multi-turn context across sessions with safety fallbacks.
- **🎨 Sleek Streamlit Interface:**
  Modern ChatGPT-inspired dark UI with custom responsive sidebar, pinned session navigation, and real-time streaming feedback.

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/) (v1.65.0)
- **AI Orchestration:** [LangChain](https://www.langchain.com/) (`langchain-google-genai`, `langchain-core`)
- **LLM Engine:** [Google Gemini](https://ai.google.dev/) (`gemini-3.5-flash` with fallback to `gemini-3.5-flash-lite`)
- **Database:** [MongoDB](https://www.mongodb.com/) via `pymongo`
- **Security & Privacy:** Local Regex PII Masking Engine
- **Language:** Python 3.10+

---

## 📁 Project Structure

```text
SpendSense AI/
├── app.py              # Streamlit web application & user interface
├── logic.py            # LangChain LCEL pipeline, Gemini models, & PII masking logic
├── database.py         # MongoDB connection, session management, and CRUD helpers
├── requirements.txt    # Project dependencies
├── logo.png            # Application logo (512x512)
├── download_logo.py    # Logo asset retrieval script
├── .env.example        # Environment variables template
└── README.md           # Documentation
```

---

> Note for Judges: For security reasons, the .env file is not uploaded to GitHub. The actual .env file containing the API keys and MongoDB URI is included securely in the official email submission ZIP folder. Please place it in the root directory before running the application.

## 🚀 How to Run

### 1. Prerequisites
Ensure you have Python 3.10 or higher installed.

### 2. Environment Configuration
Create a `.env` file in the root directory (or use the one provided in the submission ZIP folder):
```env
GEMINI_API_KEY=your_google_api_key_here
MONGO_URI=your_mongodb_connection_string_here
```

### 3. Install Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Launch Application
Start the Streamlit development server:
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 👥 Team
**WealthByte**
