# TalentScout — Intelligent Hiring Assistant 🤖

> **🚀 Live Demo:** [https://talentscout-hiring-assistant-tqwz79ka5aqcl7yrv9ebyg.streamlit.app](https://talentscout-hiring-assistant-tqwz79ka5aqcl7yrv9ebyg.streamlit.app)

TalentScout is an **AI-powered hiring assistant chatbot** that automates the initial screening phase of technical recruitment. It conducts natural, conversational interviews — collecting candidate details, detecting tech stacks, and generating tailored technical questions — all in real time. No forms, no manual effort.

Built with **Python**, **Streamlit**, and **Groq's ultra-fast cloud LLM inference** (Llama 3.1 8B — free tier).

---

## 🎯 Project Overview

TalentScout automates the initial screening phase of technical hiring. It:

- Greets candidates and collects key profile information naturally
- Detects tech stacks from conversational responses
- Generates tailored technical questions based on declared skills and experience level
- Stores structured interview data securely in JSON
- Supports GDPR-compliant data handling with anonymization capabilities

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 AI-Powered Chat | Powered by Groq + Llama 3.1 8B — near-instant responses |
| 📋 Info Extraction | Auto-extracts name, email, experience, tech stack, position |
| 💡 Dynamic Questions | Generates 3–5 questions tailored to the candidate's tech stack and seniority |
| 🔍 Tech Detection | Identifies 50+ languages, frameworks, databases and tools from conversation |
| 💾 Data Export | Saves structured candidate profiles + full chat history as JSON |
| 🔒 GDPR Compliance | PII handling, optional anonymization, data privacy notice |
| ⚡ Fast & Free | No heavy model downloads — uses Groq's free cloud inference API |

---

## 📋 Requirements

### System Requirements
- Python 3.8+
- Internet connection (for Groq API calls)
- ~50MB disk space

### Dependencies
```
streamlit
python-dotenv
groq
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/talentscout-hiring.git
cd "TalentScout HIRING"
```

### 2. Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Get a Free Groq API Key
1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up (free, no credit card required)
3. Click **"Create API Key"** and copy it

### 5. Configure Environment Variables
Create a `.env` file in the project root:
```bash
GROQ_API_KEY=gsk_your_actual_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

> **Available models:**
> - `llama-3.1-8b-instant` — Fastest (recommended)
> - `llama-3.3-70b-versatile` — More capable
> - `mixtral-8x7b-32768` — Large context window

### 6. Run the Application
```bash
streamlit run streamlit_app.py
```

The app opens at `http://localhost:8501`

---

## 💻 Usage Guide

### Starting an Interview
1. Click **"🚀 Start New Interview"** in the sidebar, or
2. Click **"🎬 Begin Interview"** on the main page

### During the Interview
- Answer questions naturally — the bot extracts info automatically
- Share your name, contact, experience years, tech stack, and desired position
- The chatbot adapts follow-up questions based on your answers

### Generating Technical Questions
1. After mentioning your tech stack, click **"🎯 Generate Technical Questions"**
2. Questions are tailored to your experience level (Junior / Mid-level / Senior / Expert)

### Finalizing & Exporting
- **"✅ Finalize Interview"** — Ends the session and saves data with a closing summary
- **"📥 Export Interview Data"** — Saves and shows your candidate profile at any point during the chat

---

## 📁 Project Structure

```
TalentScout HIRING/
├── streamlit_app.py              # Main Streamlit application & UI
├── requirements.txt              # Python dependencies
├── .env                          # API keys (not committed to git)
├── .env.example                  # Template for environment variables
├── .gitignore                    # Protects secrets & PII from git
├── README.md                     # This file
├── TECHNICAL_DETAILS.md          # Architecture & implementation details
├── src/
│   ├── __init__.py               # Package initializer
│   ├── config.py                 # Configuration, constants & tech keywords
│   ├── chatbot.py                # Core interview orchestration logic
│   ├── groq_llm.py               # Groq API client wrapper
│   ├── candidate_extractor.py    # Regex-based info extraction from chat
│   ├── prompt_engine.py          # Prompt templates & question generation
│   └── data_handler.py           # JSON storage, GDPR anonymization
└── data/
    ├── candidates.json           # Stored candidate profiles (not in git)
    └── conversations.json        # Full conversation histories (not in git)
```

---

## 🔧 Configuration

### Environment Variables (`.env`)
```bash
GROQ_API_KEY=gsk_...             # Groq API key (required)
GROQ_MODEL=llama-3.1-8b-instant  # Model selection (optional)
```

### Application Settings (`src/config.py`)
| Setting | Default | Description |
|---|---|---|
| `GROQ_MODEL` | `llama-3.1-8b-instant` | LLM model used for inference |
| `TEMPERATURE` | `0.7` | Response creativity (0.0–1.0) |
| `MAX_TOKENS` | `512` | Max response length |
| `MAX_QUESTIONS_PER_STACK` | `5` | Technical questions per interview |

---

## 🔒 Security & Privacy

### GDPR Compliance
- ✅ Data Privacy Notice shown to every candidate before interview
- ✅ PII (name, email) stored separately, removable via `anonymize_candidate_data()`
- ✅ Right to access — Export functionality gives candidates their own data
- ✅ Only necessary data collected (purpose limitation)
- ✅ `data/` folder excluded from version control via `.gitignore`

### Best Practices Implemented
- API keys stored in `.env`, never hardcoded
- `.env` excluded from git via `.gitignore`
- Candidate data files excluded from version control
- Modular architecture — data layer is independent of UI

---

## 🧠 Prompt Engineering

### System Prompt Design
The system prompt (in `src/prompt_engine.py`) instructs the model to:
1. Collect all required fields in natural order (name → contact → experience → tech stack → position)
2. Ask one question at a time to avoid overwhelming candidates
3. Adapt technical question difficulty to the declared experience level
4. Handle 50+ technologies across backend, frontend, databases, cloud, and DevOps
5. Maintain GDPR-aware data handling throughout

### Technical Question Prompt
Structured to produce:
- 3–5 questions per interview
- Each question tagged with what it assesses (conceptual / practical / architectural)
- Progressively increasing challenge level
- Coverage across the full declared tech stack

### Extraction Strategy
A hybrid approach combining:
- **Regex patterns** for structured data (email, phone, years of experience)
- **Keyword matching** against a curated database of 50+ tech terms
- **NLP-style patterns** for names (`"my name is X"`, `"I am X"`)

---

## 🐛 Challenges & Solutions

| Challenge | Solution |
|---|---|
| HuggingFace Mistral-7B was too heavy (14GB) | Replaced with Groq cloud inference — zero local download |
| `load_dotenv()` called after config import | Moved `load_dotenv()` before src imports; also added it inside `config.py` |
| `export_interview_data()` returned `None` without `finalize_interview()` | Auto-save logic added — export now works at any point |
| Name extraction was missing entirely | Added regex patterns for common name-introduction phrases |
| OpenAI key was hardcoded in `.env` by mistake | Switched to Groq, removed old key, added `.gitignore` |

---

## 🚀 Deployment

### Local (Development)
```bash
venv\Scripts\streamlit run streamlit_app.py
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Streamlit Cloud (Recommended Free Option)
1. Push project to GitHub (`.env` is gitignored — add `GROQ_API_KEY` in Streamlit Cloud Secrets)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → select `streamlit_app.py` → Deploy

### AWS / GCP
- **AWS**: Deploy container to ECS Fargate or EC2 with the Dockerfile above
- **GCP**: Use Cloud Run — `gcloud run deploy` with the Docker image

---

## 📝 License

This project is developed as part of a technical assessment for TalentScout Inc.

---

**Last Updated**: April 10, 2026
**Version**: 1.1.0
**LLM Backend**: Groq — Llama 3.1 8B Instant
**Status**: Production Ready ✅
